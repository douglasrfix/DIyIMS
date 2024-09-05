import configparser
import sys
from pathlib import Path

from rich import print


def install_app():
    if sys.platform.startswith("freebsd"):
        print("FreeBSD found and not tested")
        return 1
    elif sys.platform.startswith("linux"):
        print("Linux found and not tested")
        return 1
    elif sys.platform.startswith("aix"):
        print("AIX found and not supported")
        return 1
    elif sys.platform.startswith("wasi"):
        print("WASI found and not supported")
        return 1
    elif sys.platform.startswith("win32"):
        print("Windows found and supported")
    elif sys.platform.startswith("cygwin"):
        print("CYGWIN found and not supported")
        return 1
    elif sys.platform.startswith("darwin"):
        print("macOS found and not supported")
        return 1
    else:
        print("OS not identified and thus not supported")

    directory_path = Path.home().joinpath(
        "AppData",
        "Local",
        "diyims",
    )
    if directory_path.exists():
        print("Previous installation found. Current installation not performed.")
        return 1

    directory_path.mkdir(mode=755, parents=True, exist_ok=True)
    file_path = Path().joinpath(directory_path, "diyims")
    default_db_path = str(Path.home() / ".diyims")

    config = configparser.ConfigParser()
    config["Paths"] = {}
    config["Paths"]["db_path"] = default_db_path
    with open(file_path, "w") as configfile:
        config.write(configfile)
    return 0
