import configparser
import json
from pathlib import Path

import requests
from rich import print

from diyims.error_classes import InvalidDriveLetterError, PreExistingInstallationError
from diyims.paths import get_path_dict
from diyims.urls import get_url_dict


def install_app(drive_letter, force_python):
    url_dict = get_url_dict()

    path_dict = get_path_dict(drive_letter, force_python)

    ini_path = path_dict["ini_path"]
    db_path = path_dict["db_path"]
    log_path = path_dict["log_path"]
    header_path = path_dict["header_path"]
    peer_path = path_dict["peer_path"]

    if ini_path.exists():
        raise (PreExistingInstallationError(""))

    try:
        db_path.mkdir(mode=755, parents=True, exist_ok=True)
    except FileNotFoundError:
        raise (InvalidDriveLetterError(drive_letter))

    ini_path.mkdir(mode=755, parents=True, exist_ok=True)
    log_path.mkdir(mode=755, parents=True, exist_ok=True)
    header_path.mkdir(mode=755, parents=True, exist_ok=True)
    peer_path.mkdir(mode=755, parents=True, exist_ok=True)

    ini_file = Path(ini_path).joinpath("diyims.ini")
    db_file = Path(db_path).joinpath("diyims.db")
    header_file = Path(header_path).joinpath("header.json")
    peer_file = Path(header_path).joinpath("peer_table.json")

    with requests.post(url_dict["id"], stream=False) as r:
        json_dict = json.loads(r.text)

    config = configparser.ConfigParser()
    config["Paths"] = {}
    config["Drives"] = {}
    config["IPFS"] = {}
    config["Paths"]["ini_path"] = str(ini_file)
    config["Paths"]["db_path"] = str(db_file)
    config["Paths"]["log_path"] = str(log_path)
    config["Drives"]["default_drive"] = str(path_dict["default_drive"])
    config["Drives"]["drive_letter"] = str(path_dict["drive_letter"])
    config["Paths"]["header_path"] = str(header_file)
    config["Paths"]["peer_path"] = str(peer_file)
    config["IPFS"]["agent"] = json_dict["AgentVersion"]
    with open(ini_file, "w") as configfile:
        config.write(configfile)
    print("Installation Complete")

    return 0
