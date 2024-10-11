import os
from pathlib import Path


def get_linux_template_dict():
    try:
        xdg_home = Path(os.environ["OVERRIDE_HOME"])  # NOTE: need test for this

    except KeyError:
        xdg_home = Path.home()

    xdg_data_home = Path(xdg_home).joinpath(".local", "share", "diyims", "Data")
    xdg_config_home = Path(xdg_home).joinpath(".config", "diyims", "Config")
    xdg_cache_home = Path(xdg_home).joinpath(".cache", "diyims", "Cache")
    xdg_state_home = Path(xdg_home).joinpath(".local", "state", "diyims", "State")

    template_path_dict = {}
    template_path_dict["config_path"] = xdg_config_home
    template_path_dict["db_path"] = xdg_data_home
    template_path_dict["log_path"] = xdg_state_home
    template_path_dict["header_path"] = xdg_cache_home
    template_path_dict["peer_path"] = xdg_cache_home

    return template_path_dict
