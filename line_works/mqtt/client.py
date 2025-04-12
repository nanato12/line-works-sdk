import asyncio
import json
from ssl import create_default_context
from types import TracebackType
from typing import Callable, Self

import websockets
from pydantic import BaseModel, PrivateAttr
from websockets.asyncio.client import ClientConnection

from line_works.client import LineWorks
from line_works.logger import get_file_path_logger
from line_works.mqtt import config
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.exceptions import (
    LineWorksMQTTException,
    PacketParseException,
)
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.packets import ConnectionPacket

logger = get_file_path_logger(__name__)


class MQTTClient(BaseModel):
    works: LineWorks
    _trace_func: dict[PacketType, Callable[[LineWorks, MQTTPacket], None]] = (
        PrivateAttr(default_factory=dict)
    )
    _ws: ClientConnection = PrivateAttr(default=None)
    _unique_ids: list[str] = PrivateAttr(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def add_trace_func(
        self,
        packet_type: PacketType,
        f: Callable[[LineWorks, MQTTPacket], None],
    ) -> None:
        self._trace_func[packet_type] = f

    async def connect(self) -> None:
        self._ws = await websockets.connect(
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

        await self._ws.send(ConnectionPacket().generate())

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.__send_keepalive())
            tg.create_task(self.__listen())

    async def disconnect(self) -> None:
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

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

    async def __send_keepalive(self) -> None:
        while True:
            status_message = json.dumps(
                {"type": "presence", "payload": "WEB_ONLINE"}
            )
            await self._ws.send(status_message)
            await self._ws.send("keepalive")
            await asyncio.sleep(config.KEEP_ALIVE_INTERVAL_SEC)

    async def __listen(self) -> None:
        while True:
            message = await self._ws.recv()
            if isinstance(message, bytes):
                await self.__handle_binary_message(message)
            else:
                logger.debug(f"Received a non-binary message: {message}")

    async def __handle_binary_message(self, message: bytes) -> None:
        try:
            packet = MQTTPacket.parse_from_bytes(message)

            if packet.type == PacketType.PINGRESP:
                return

            if packet.type == PacketType.PUBLISH:
                try:
                    p = packet.payload
                    if p.unique_id in self._unique_ids:
                        return
                    elif p.unique_id:
                        self._unique_ids.append(p.unique_id)
                except PacketParseException as e:
                    logger.debug("packet parse error", exc_info=e)

            logger.debug(f"{packet=}")

            if f := self._trace_func.get(packet.type):
                f(self.works, packet)
        except LineWorksMQTTException as e:
            logger.error(
                "Error while handling binary message. "
                "Failed to parse or process the MQTT packet.",
                exc_info=e,
            )
        except Exception as e:
            logger.error("error", exc_info=e)
