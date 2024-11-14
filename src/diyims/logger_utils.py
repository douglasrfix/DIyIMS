import logging
from logging.handlers import RotatingFileHandler
from diyims.path_utils import get_path_dict


def get_logger():
    path_dict = get_path_dict()

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")
    formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel("INFO")

    file_handler = RotatingFileHandler(
        path_dict["log_file"],
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
