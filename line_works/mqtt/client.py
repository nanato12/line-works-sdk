import asyncio
import inspect
import json
import socket
import time
from collections import OrderedDict
from ssl import create_default_context
from types import TracebackType
from typing import Awaitable, Callable, Optional, Self, Union

import websockets
from pydantic import BaseModel, Field, PrivateAttr
from websockets.asyncio.client import ClientConnection
from websockets.exceptions import ConnectionClosed

from line_works.client import LineWorks
from line_works.logger import get_file_path_logger
from line_works.mqtt import config
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.exceptions import (
    LineWorksMQTTException,
    MQTTConnectionLost,
    MQTTConnectionRefused,
    PacketParseException,
)
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.packets import (
    ConnectionPacket,
    PingReqPacket,
    PubAckPacket,
    PubCompPacket,
    PubRecPacket,
)
from line_works.mqtt.stream import MQTTStreamParser

logger = get_file_path_logger(__name__)

# トレース関数は同期でも非同期でもよい
TraceFunc = Callable[[LineWorks, MQTTPacket], Union[None, Awaitable[None]]]


class MQTTClient(BaseModel):
    """LINE WORKS の通知用 MQTT (over WebSocket) クライアント。

    `connect()` は接続が終わるまで戻らない。`disconnect()` で閉じた場合は
    正常終了し、それ以外 (サーバ切断、無通信タイムアウトなど) は例外を
    送出する。再接続はしないので、必要なら `LineWorksTracer.run()` を使うか
    呼び出し側でループする。

    サーバは通知以外なにも送ってこないので、`idle_timeout` は既定で無効。
    死んだ接続は TCP keepalive (カーネル) とサーバ側のクローズで検出する。
    """

    works: LineWorks
    keepalive_interval: float = Field(
        default=config.KEEP_ALIVE_INTERVAL_SEC, gt=0
    )
    idle_timeout: Optional[float] = Field(
        default=config.IDLE_TIMEOUT_SEC, gt=0
    )
    dedupe_cache_size: int = Field(default=config.DEDUPE_CACHE_SIZE, ge=0)

    _trace_func: dict[PacketType, TraceFunc] = PrivateAttr(
        default_factory=dict
    )
    _ws: Optional[ClientConnection] = PrivateAttr(default=None)
    _parser: MQTTStreamParser = PrivateAttr(default_factory=MQTTStreamParser)
    _seen_unique_ids: "OrderedDict[str, None]" = PrivateAttr(
        default_factory=OrderedDict
    )
    _connected: bool = PrivateAttr(default=False)
    _close_requested: bool = PrivateAttr(default=False)
    _last_received_at: Optional[float] = PrivateAttr(default=None)

    class Config:
        arbitrary_types_allowed = True

    @property
    def is_connected(self) -> bool:
        """CONNACK を受け取り、まだ切断されていない"""
        return self._connected

    @property
    def last_received_at(self) -> Optional[float]:
        """最後に何か受信した時刻 (time.monotonic())"""
        return self._last_received_at

    def add_trace_func(
        self,
        packet_type: PacketType,
        f: TraceFunc,
    ) -> None:
        self._trace_func[packet_type] = f

    async def connect(self) -> None:
        self._close_requested = False
        self._connected = False
        self._parser.reset()

        ws = await websockets.connect(
            config.HOST,
            ssl=create_default_context(),
            additional_headers={
                "Cookie": self.works.cookie_str,
                **config.HEADERS,
            },
            subprotocols=["mqtt"],
            ping_interval=None,
            ping_timeout=None,
        )
        self._ws = ws
        self._last_received_at = time.monotonic()
        self.__enable_tcp_keepalive(ws)

        try:
            await ws.send(ConnectionPacket().generate())

            listen = asyncio.create_task(self.__listen(ws))
            keepalive = asyncio.create_task(self.__send_keepalive(ws))
            try:
                done, _ = await asyncio.wait(
                    {listen, keepalive},
                    return_when=asyncio.FIRST_COMPLETED,
                )
            finally:
                listen.cancel()
                keepalive.cancel()
                await asyncio.gather(listen, keepalive, return_exceptions=True)

            for task in done:
                exc = task.exception()
                if exc is None:
                    continue
                if isinstance(exc, ConnectionClosed) and self._close_requested:
                    logger.info("MQTT connection closed by request")
                    return
                raise exc
        finally:
            self._connected = False
            self._ws = None
            await self.__close(ws)

    async def disconnect(self) -> None:
        self._close_requested = True
        ws = self._ws
        if ws is not None:
            await self.__close(ws)

    async def __close(self, ws: ClientConnection) -> None:
        try:
            await asyncio.wait_for(
                ws.close(), timeout=config.CLOSE_TIMEOUT_SEC
            )
        except Exception as e:
            logger.debug(f"Error while closing websocket: {e!r}")

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.disconnect()

    @staticmethod
    def __enable_tcp_keepalive(ws: ClientConnection) -> None:
        try:
            sock = ws.transport.get_extra_info("socket")
            if sock is None:
                return
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            for name, value in (
                ("TCP_KEEPIDLE", config.TCP_KEEPALIVE_IDLE_SEC),
                ("TCP_KEEPINTVL", config.TCP_KEEPALIVE_INTERVAL_SEC),
                ("TCP_KEEPCNT", config.TCP_KEEPALIVE_COUNT),
            ):
                option = getattr(socket, name, None)
                if option is not None:
                    sock.setsockopt(socket.IPPROTO_TCP, option, value)
        except Exception as e:
            logger.debug(f"Could not enable TCP keepalive: {e!r}")

    async def __send_keepalive(self, ws: ClientConnection) -> None:
        status_message = json.dumps(
            {"type": "presence", "payload": "WEB_ONLINE"}
        )
        ping_req = PingReqPacket().generate()
        while True:
            await ws.send(status_message)
            await ws.send("keepalive")
            await ws.send(ping_req)
            await asyncio.sleep(self.keepalive_interval)

    async def __listen(self, ws: ClientConnection) -> None:
        while True:
            try:
                message = await asyncio.wait_for(
                    ws.recv(), timeout=self.idle_timeout
                )
            except TimeoutError:
                raise MQTTConnectionLost(
                    f"No data received for {self.idle_timeout:.0f} seconds"
                ) from None
            self._last_received_at = time.monotonic()

            if not isinstance(message, bytes):
                logger.debug(f"Received a non-binary message: {message!r}")
                continue

            try:
                packets = self._parser.feed(message)
            except PacketParseException as e:
                raise MQTTConnectionLost(
                    f"MQTT stream is out of sync: {e}"
                ) from e

            for raw in packets:
                await self.__handle_packet(ws, raw)

    async def __handle_packet(self, ws: ClientConnection, raw: bytes) -> None:
        try:
            packet = MQTTPacket.parse_from_bytes(raw)
        except PacketParseException as e:
            logger.warning(f"Failed to parse MQTT packet: {e}")
            return

        if packet.type == PacketType.CONNACK:
            self.__handle_connack(packet)
        elif packet.type == PacketType.PINGRESP:
            return
        elif packet.type == PacketType.PUBLISH:
            await self.__acknowledge_publish(ws, packet)
            if self.__is_duplicate(packet):
                logger.debug(f"Dropped duplicate PUBLISH: {packet!r}")
                return
        elif packet.type == PacketType.PUBREL:
            await self.__complete_publish(ws, packet)
        elif packet.type == PacketType.DISCONNECT:
            raise MQTTConnectionLost("Server sent DISCONNECT")

        logger.debug(f"{packet=}")
        await self.__dispatch(packet)

    def __handle_connack(self, packet: MQTTPacket) -> None:
        payload = packet.raw_payload or b""
        return_code = payload[1] if len(payload) >= 2 else None
        if return_code != 0:
            raise MQTTConnectionRefused(
                f"Connection refused by server (return code={return_code})"
            )
        self._connected = True
        logger.info("MQTT connected")

    async def __acknowledge_publish(
        self, ws: ClientConnection, packet: MQTTPacket
    ) -> None:
        try:
            qos = packet.qos
            packet_id = packet.packet_id
        except PacketParseException as e:
            logger.warning(f"Cannot acknowledge PUBLISH: {e}")
            return
        if packet_id is None:
            return
        if qos == 1:
            await ws.send(PubAckPacket(packet_id).generate())
        elif qos == 2:
            await ws.send(PubRecPacket(packet_id).generate())

    async def __complete_publish(
        self, ws: ClientConnection, packet: MQTTPacket
    ) -> None:
        try:
            packet_id = packet.packet_id
        except PacketParseException as e:
            logger.warning(f"Cannot complete PUBREL: {e}")
            return
        if packet_id is not None:
            await ws.send(PubCompPacket(packet_id).generate())

    def __is_duplicate(self, packet: MQTTPacket) -> bool:
        if self.dedupe_cache_size == 0:
            return False
        try:
            unique_id = packet.payload.unique_id
        except (PacketParseException, ValueError) as e:
            logger.debug(f"packet payload is not deduplicable: {e}")
            return False
        if not unique_id:
            return False
        if unique_id in self._seen_unique_ids:
            return True
        self._seen_unique_ids[unique_id] = None
        while len(self._seen_unique_ids) > self.dedupe_cache_size:
            self._seen_unique_ids.popitem(last=False)
        return False

    async def __dispatch(self, packet: MQTTPacket) -> None:
        f = self._trace_func.get(packet.type)
        if f is None:
            return
        try:
            result = f(self.works, packet)
            if inspect.isawaitable(result):
                await result
        except LineWorksMQTTException as e:
            logger.warning(
                f"Trace function could not process {packet.type.name}: {e}"
            )
        except Exception:
            logger.exception(
                f"Unhandled error in trace function for {packet.type.name}"
            )
