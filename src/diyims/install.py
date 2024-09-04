import sys
from pathlib import Path

# import configparser
from rich import print


def install():
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

    # config = configparser.ConfigParser()

    directory_path = Path.home().joinpath("AppData", "local", "diyims, diyims.ini")
    if directory_path.exists():
        print("Previous installation found. Current installation not performed.")
        return 1

    directory_path.mkdir(parents=True, exist_ok=True)
    return 0

    # with open("diyims.ini", "w") as configfile:
    #     config.write(configfile)
