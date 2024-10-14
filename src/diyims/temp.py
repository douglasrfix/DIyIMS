"""
import sys

# major
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

# minor
if sys.version_info[1] > 8:
    raise Exception("Must be Python 3.9 or greater")


str = importlib.resources.read_text(
    package, resource, encoding="utf-8", errors="strict"
)
lexicon = json.load(importlib.resources.open_text("mypackagename", "data/lexicon.json"))

p = importlib.resources.as_file(
    importlib.resources.files("resources") / "resource.toml"
)

with p as f:
    my_toml = tomllib.load(f.open("rb"))  # as an example

from sqlite3 import Error, IntegrityError


    if sys.platform.startswith("freebsd"):
        print("FreeBSD(a descendent of the Berkley Software Distribution) found and not tested")
        return 1
    elif sys.platform.startswith("linux"):
        print("Linux(a family of unix like environments using the Linux kernel from Linus Torvalds) found and not tested")
        return 1
    elif sys.platform.startswith("aix"):
        print("AIX(IBM Unix variant)  found and not supported")
        return 1
    elif sys.platform.startswith("wasi"):
        print("WASI(Web Assembly) found and not supported")
        return 1
    elif sys.platform.startswith("win32"):
        path_dict = get_path()
        print(path_dict)
        print("Windows found and supported")
        directory_path = Path.home().joinpath(
            "AppData",
            "Local",
            "diyims",
        )
    elif sys.platform.startswith("cygwin"):
        print("CYGWIN(Unix like environment for Windows) found and not supported")
        return 1
    elif sys.platform.startswith("darwin"):
        print("macOS found and not supported")
        return 1
    else:
        print("OS not identified and thus not supported")
"""
# C:\Users\<USER>\AppData\[Local/Roaming]\YourProgram\logs\
# $HOME/.local/state should be used.
#  ~/.local/share/myprogram/logs per xdg spec environment variables


# default_db_path = str(Path.home() / ".diyims")

#   3config = configparser.ConfigParser()
# config["Paths"] = {}
# config["Paths"]["db_path"] = path_dict["db_path"]
# with open(file_path, "w") as configfile:
#    config.write(configfile)
# return 0
