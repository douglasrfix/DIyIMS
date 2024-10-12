import configparser
from pathlib import Path

from diyims.error_classes import ApplicationNotInstalledError
from diyims.os_platform import test_os_platform
from diyims.posix_path import get_linux_template_dict
from diyims.windows_path import get_win32_template_dict


def get_install_template_dict():
    os_platform = test_os_platform()

    if os_platform.startswith("win32"):
        install_template_dict = get_win32_template_dict()

    elif os_platform.startswith("linux"):
        install_template_dict = get_linux_template_dict()

    return install_template_dict


def get_path_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    path_dict = {}
    path_dict["config_path"] = Path(parser["Paths"]["config_path"])
    path_dict["config_file"] = Path(parser["Files"]["config_file"])
    path_dict["db_path"] = Path(parser["Paths"]["db_path"])
    path_dict["db_file"] = Path(parser["Files"]["db_file"])
    path_dict["log_path"] = Path(parser["Paths"]["log_path"])
    path_dict["header_path"] = Path(parser["Paths"]["header_path"])
    path_dict["header_file"] = Path(parser["Files"]["header_file"])
    path_dict["peer_path"] = Path(parser["Paths"]["peer_path"])
    path_dict["peer_file"] = Path(parser["Files"]["peer_file"])

    return path_dict
