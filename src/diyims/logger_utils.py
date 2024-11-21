import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from diyims.path_utils import get_path_dict


def get_logger(file):
    path_dict = get_path_dict()

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")
    formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel("INFO")  # NOTE: get logging levels from config

    file_handler = RotatingFileHandler(
        Path(path_dict["log_path"]).joinpath(file),
        mode="a",
        maxBytes=100000,
        backupCount=1,
        encoding="utf-8",
        delay=False,
        errors=None,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel("DEBUG")

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
