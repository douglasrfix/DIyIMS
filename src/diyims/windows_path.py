"""
This module provides the knowledge to navigate the installation paths used by
the various supported platforms.

The primary challenge to the developer is the lack of real standards. Most of
traditional placement of files is based upon historical conventions and
practices established early in the history of the platform and even the
computing industry itself.

These standards were not intended for single user machines with no
administrative support. With this in mind, and through the luck of the search
engine draw, I have modeled my placement based upon a go implementation of the
XDG specification. (https://pkg.go.dev/github.com/adrg/xdg)

Given the lack of a convenient method of detecting the version of windows,
the choice between %AppData% and %LocalAppData% was in favor %AppData% for
legacy versions support.

All of the files are placed in user spaces to minimize permission issues.
"""


import os
from pathlib import Path


def get_win32_template_dict():
    try:
        xdg_home = Path(os.environ["OVERRIDE_HOME"])

    except KeyError:
        xdg_home = Path(os.environ["UserProfile"])

    xdg_data_home = Path(xdg_home).joinpath("AppData", "Roaming", "diyims", "Data")
    xdg_config_home = Path(xdg_home).joinpath("AppData", "Roaming", "diyims", "Config")
    xdg_cache_home = Path(xdg_home).joinpath("AppData", "Roaming", "diyims", "Cache")
    xdg_state_home = Path(xdg_home).joinpath("AppData", "Roaming", "diyims", "State")

    template_path_dict = {}
    template_path_dict["config_path"] = xdg_config_home
    template_path_dict["db_path"] = xdg_data_home
    template_path_dict["log_path"] = xdg_state_home
    template_path_dict["header_path"] = xdg_cache_home
    template_path_dict["peer_path"] = xdg_cache_home

    return template_path_dict
