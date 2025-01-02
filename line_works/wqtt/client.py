import asyncio
from ssl import create_default_context

import websockets
from pydantic import BaseModel, PrivateAttr
from requests.cookies import RequestsCookieJar
from websockets.asyncio.client import ClientConnection

from line_works.wqtt import config, packets


class WMQTTClient(BaseModel):
    cookies: RequestsCookieJar
    _ws: ClientConnection = PrivateAttr(default=None)

    class Config:
        arbitrary_types_allowed = True

    @property
    def cookie_str(self) -> str:
        return "; ".join(f"{k}={v}" for k, v in self.cookies.items())

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
                await self._handle_binary_message(message)
            else:
                print(f"テキストメッセージを受信: {message}")

    async def _handle_binary_message(self, message: bytes) -> None:
        # TODO: 実装
        pass
