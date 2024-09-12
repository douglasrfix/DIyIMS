import configparser
from pathlib import Path

from rich import print

from diyims.error_classes import UnSupportedPlatformError, UnTestedPlatformError
from diyims.paths import get_path_dict


def install_app(drive_letter, force_python):
    try:
        path_dict = get_path_dict(drive_letter, force_python)

    except UnSupportedPlatformError as error:
        print(error.value, "is an unsupported platform")
        return

    except UnTestedPlatformError as error:
        print(
            error.system,
            error.release,
            "is an untested platform if Python was installed via the Microsoft Store application.",
        )
        return

    ini_path = path_dict["ini_path"]
    db_path = path_dict["db_path"]
    log_path = path_dict["log_path"]
    header_path = path_dict["header_path"]
    peer_path = path_dict["peer_path"]
    if ini_path.exists():
        print("Previous installation found. Current installation not performed.")
        return 0

    try:
        db_path.mkdir(mode=755, parents=True, exist_ok=True)
    except FileNotFoundError:
        print(f"Drive letter {drive_letter} invalid.")
        return

    ini_path.mkdir(mode=755, parents=True, exist_ok=True)
    log_path.mkdir(mode=755, parents=True, exist_ok=True)
    header_path.mkdir(mode=755, parents=True, exist_ok=True)
    peer_path.mkdir(mode=755, parents=True, exist_ok=True)

    ini_file = Path(ini_path).joinpath("diyims.ini")
    db_file = Path(db_path).joinpath("diyims.db")
    header_file = Path(header_path).joinpath("header.json")
    peer_file = Path(header_path).joinpath("peer_table.json")

    config = configparser.ConfigParser()
    config["Paths"] = {}
    config["Drives"] = {}
    config["Paths"]["ini_path"] = str(ini_file)
    config["Paths"]["db_path"] = str(db_file)
    config["Paths"]["log_path"] = str(log_path)
    config["Drives"]["default_drive"] = str(path_dict["default_drive"])
    config["Drives"]["drive_letter"] = str(path_dict["drive_letter"])
    config["Paths"]["header_path"] = str(header_file)
    config["Paths"]["peer_path"] = str(peer_file)
    with open(ini_file, "w") as configfile:
        config.write(configfile)
    return 0
