import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from diyims.path_utils import get_path_dict
from diyims.config_utils import get_logger_config_dict


def get_logger(file):
    logger_config_dict = get_logger_config_dict()
    path_dict = get_path_dict()

    logger = logging.getLogger(__name__)
    logger.setLevel(logger_config_dict["default_level"])
    formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logger_config_dict["console_level"])

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
    file_handler.setLevel(logger_config_dict["file_level"])

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
