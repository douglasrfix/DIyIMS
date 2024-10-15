import configparser
import json
import os
import platform
from pathlib import Path

import requests
from rich import print

from diyims.error_classes import (
    InvalidDriveLetterError,
    PreExistingInstallationError,
    UnSupportedPlatformError,
    UnTestedPlatformError,
)
from diyims.os_platform import test_os_platform
from diyims.path_utils import get_install_template_dict
from diyims.url_utils import get_url_dict


def install_app(drive_letter, force_install):
    try:
        os_platform = test_os_platform()

    except UnSupportedPlatformError:
        raise

    override_drive = "False"
    if drive_letter != "Default" and os_platform == "win32":
        if Path(drive_letter + "/").exists() is not True:
            try:
                override_drive = os.environ["OVERRIDE_DRIVE"]

            except KeyError:
                raise (InvalidDriveLetterError(drive_letter))

    try:
        python_release = os.environ["OVERRIDE_RELEASE"]

    except KeyError:
        python_release = platform.release()

    if int(python_release) >= 10 and os_platform == "win32" and force_install is False:
        raise UnTestedPlatformError(platform.system(), platform.release())

    install_template_dict = get_install_template_dict()

    if drive_letter != "Default":
        if drive_letter != Path(install_template_dict["db_path"]).drive:
            install_template_dict["db_path"] = Path(drive_letter + "/").joinpath(
                "diyims", "Data"
            )

    config_path = install_template_dict["config_path"]
    db_path = install_template_dict["db_path"]
    log_path = install_template_dict["log_path"]
    header_path = install_template_dict["header_path"]
    peer_path = install_template_dict["peer_path"]

    config_file = Path(config_path).joinpath("diyims.ini")
    if config_file.exists():
        raise (PreExistingInstallationError(" "))

    if override_drive != "True":
        db_path.mkdir(mode=755, parents=True, exist_ok=True)

    config_path.mkdir(mode=755, parents=True, exist_ok=True)
    log_path.mkdir(mode=755, parents=True, exist_ok=True)
    header_path.mkdir(mode=755, parents=True, exist_ok=True)
    peer_path.mkdir(mode=755, parents=True, exist_ok=True)

    db_file = Path(db_path).joinpath("diyims.db")
    header_file = Path(header_path).joinpath("header.json")
    peer_file = Path(header_path).joinpath("peer_table.json")

    url_dict = get_url_dict()
    with requests.post(url_dict["id"], stream=False) as r:
        json_dict = json.loads(r.text)

    parser = configparser.ConfigParser()
    parser["Paths"] = {}
    parser["Files"] = {}
    parser["IPFS"] = {}
    parser["Paths"]["config_path"] = str(config_path)
    parser["Files"]["config_file"] = str(config_file)
    parser["Paths"]["db_path"] = str(db_path)
    parser["Files"]["db_file"] = str(db_file)
    parser["Paths"]["log_path"] = str(log_path)
    parser["Paths"]["header_path"] = str(header_path)
    parser["Files"]["header_file"] = str(header_file)
    parser["Paths"]["peer_path"] = str(peer_path)
    parser["Files"]["peer_file"] = str(peer_file)
    parser["IPFS"]["agent"] = json_dict["AgentVersion"]
    with open(config_file, "w") as configfile:
        parser.write(configfile)
    print("Installation Complete")

    return 0
