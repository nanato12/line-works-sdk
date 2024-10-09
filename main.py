import logging
from logging import StreamHandler, basicConfig
from logging.handlers import TimedRotatingFileHandler
from os import makedirs

from app.logger import get_file_path_logger

LOG_DIRECTORY = "logs"

logger = get_file_path_logger(__name__)

if __name__ == "__main__":
    makedirs(LOG_DIRECTORY, exist_ok=True)

    basicConfig(
        level=logging.INFO,
        datefmt="%Y/%m/%d %H:%M:%S",
        format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)s %(message)s",
        handlers=[
            TimedRotatingFileHandler(
                f"{LOG_DIRECTORY}/app.log",
                when="midnight",
                backupCount=30,
                interval=1,
                encoding="utf-8",
            ),
            StreamHandler(),
        ],
    )

    logger.info("hello.")
