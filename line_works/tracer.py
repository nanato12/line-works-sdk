import asyncio
import time

from pydantic import Field

from line_works.logger import get_file_path_logger
from line_works.mqtt import config
from line_works.mqtt.client import MQTTClient

logger = get_file_path_logger(__name__)


class LineWorksTracer(MQTTClient):
    """再接続つきの MQTT クライアント"""

    reconnect_backoff_max: float = Field(
        default=config.RECONNECT_BACKOFF_MAX_SEC, gt=0
    )

    async def run(self, reconnect: bool = True) -> None:
        """切断されても再接続しながら受信し続ける。

        `disconnect()` が呼ばれると戻る。再接続前にセッションの有効性を
        確認し、必要なら再ログインする。
        """
        backoff = 1.0
        while not self._close_requested:
            connected_at = time.monotonic()
            try:
                await self.connect()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"MQTT connection lost: {e!r}")
            if not reconnect or self._close_requested:
                return

            if time.monotonic() - connected_at > config.STABLE_CONNECTION_SEC:
                backoff = 1.0
            logger.info(f"Reconnecting to MQTT in {backoff:.0f}s")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, self.reconnect_backoff_max)

            try:
                await asyncio.to_thread(self.works.ensure_login)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"Failed to verify LINE WORKS session: {e!r}")

    def trace(self, reconnect: bool = True) -> None:
        asyncio.run(self.run(reconnect=reconnect))
