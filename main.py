import logging
from logging import StreamHandler, basicConfig
from logging.handlers import TimedRotatingFileHandler
from os import environ, makedirs

from dotenv import load_dotenv

from line_works.client import LineWorks
from logger import get_file_path_logger

LOG_DIRECTORY = "logs"
makedirs(LOG_DIRECTORY, exist_ok=True)

load_dotenv(".env", verbose=True)

WORKS_ID = environ["WORKS_ID"]
PASSWORD = environ["PASSWORD"]

if __name__ == "__main__":
    logger = get_file_path_logger(__name__)
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

    works = LineWorks(works_id=WORKS_ID, password=PASSWORD)
    my_info = works.get_my_info()
    logger.info(f"{my_info=}")
