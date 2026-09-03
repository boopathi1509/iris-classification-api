import logging
from logging.handlers import RotatingFileHandler
from app.config import settings


logger = logging.getLogger("ml_api")


def setup_logging():
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)