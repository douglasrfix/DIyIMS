import configparser
import platform
import sys
from pathlib import Path

from diyims.error_classes import UnSupportedPlatformError, UnTestedPlatformError


def get_path_dict(drive_letter="Default", force_python=False):
    if sys.platform.startswith("win"):
        home_path = Path.home()
        home_path_parts = home_path.parts
        default_drive = Path(*home_path_parts[0:1])
        if drive_letter == "Default":
            home_drive = Path(*home_path_parts[0:1])
        else:
            home_drive = drive_letter + ":/"

        partial_home_path = Path(*home_path_parts[1 : len(home_path_parts)])
        ini_path = Path(default_drive).joinpath(
            partial_home_path,
            "AppData",
            "Local",
            "diyims",
        )
        data_path = Path(home_drive).joinpath(
            partial_home_path,
            "AppData",
            "Local",
            "diyims",
        )

    else:
        raise (UnSupportedPlatformError(sys.platform))

    config_path = Path().joinpath(ini_path, "config", "diyims.ini")
    config = configparser.ConfigParser()
    try:
        with open(config_path, "r") as configfile:
            config.read_file(configfile)

    except FileNotFoundError:
        path_dict = {}
        path_dict["ini_path"] = Path().joinpath(ini_path, "config")
        path_dict["default_drive"] = default_drive
        path_dict["drive_letter"] = home_drive
        path_dict["db_path"] = Path().joinpath(data_path, "database")
        path_dict["log_path"] = Path().joinpath(data_path, "logs")
        path_dict["header_path"] = Path().joinpath(data_path, "files")
        path_dict["peer_path"] = Path().joinpath(data_path, "files")

    else:
        path_dict = {}
        path_dict["ini_path"] = Path(config["Paths"]["ini_path"])
        path_dict["default_drive"] = Path(config["Drives"]["default_drive"])
        path_dict["drive_letter"] = Path(config["Drives"]["drive_letter"])
        path_dict["db_path"] = Path(config["Paths"]["db_path"])
        path_dict["log_path"] = Path(config["Paths"]["log_path"])
        path_dict["header_path"] = Path(config["Paths"]["header_path"])
        path_dict["peer_path"] = Path(config["Paths"]["peer_path"])

    if sys.platform.startswith("win"):
        if platform.release() >= "10":
            if not force_python:
                raise (
                    UnTestedPlatformError(
                        platform.system(), platform.release(), path_dict
                    )
                )

    return path_dict
