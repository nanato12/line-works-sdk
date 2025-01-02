import asyncio
from ssl import create_default_context

import websockets
from pydantic import BaseModel, PrivateAttr
from websockets.asyncio.client import ClientConnection

from line_works.client import LineWorks
from line_works.mqtt import config, packets
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.exceptions import LineWorksMQTTException
from line_works.mqtt.models.packet import MQTTPacket
from logger import get_file_path_logger

logger = get_file_path_logger(__name__)


class MQTTClient(BaseModel):
    works: LineWorks
    _ws: ClientConnection = PrivateAttr(default=None)
    _notification_ids: list[str] = PrivateAttr(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @property
    def cookie_str(self) -> str:
        return "; ".join(
            f"{k}={v}" for k, v in self.works.session.cookies.items()
        )

    async def connect(self) -> None:
        self._ws = await websockets.connect(
            config.HOST,
            ssl=create_default_context(),
            additional_headers={"Cookie": self.cookie_str, **config.HEADERS},
            subprotocols=["mqtt"],
            ping_interval=None,
        )

        await self._ws.send(packets.CONNECTION_PACKET)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.__send_pingreq())
            tg.create_task(self.__listen())

    async def __send_pingreq(self) -> None:
        while True:
            await asyncio.sleep(config.KEEPALIVE_INTERVAL_SEC)
            await self._ws.send(packets.PINGREQ_PACKET)

    async def __listen(self) -> None:
        while True:
            message = await self._ws.recv()
            if isinstance(message, bytes):
                await self.__handle_binary_message(message)
            else:
                logger.debug(f"Received a non-binary message: {message}")

    async def __handle_binary_message(self, message: bytes) -> None:
        try:
            p = MQTTPacket.parse_from_bytes(message)
            if p.type == PacketType.PINGRESP:
                return

            # logger.info(f"{p=}")
            if p.type == PacketType.PUBLISH:
                m = p.message
                if m.notification_id not in self._notification_ids:
                    logger.info(f"{p.message=}")
                    self._notification_ids.append(m.notification_id)
        except LineWorksMQTTException as e:
            logger.error(
                "Error while handling binary message. "
                "Failed to parse or process the MQTT packet.",
                exc_info=e,
            )
        except Exception as e:
            logger.info(f"{p=}")
            logger.error("error", exc_info=e)
