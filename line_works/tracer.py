import asyncio

from line_works.mqtt.client import MQTTClient


class LineWorksTracer(MQTTClient):
    def trace(self) -> None:
        asyncio.run(self.connect())
