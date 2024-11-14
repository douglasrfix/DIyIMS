import json
import sqlite3
import configparser
import aiosql
import requests
from time import sleep
from pathlib import Path
from diyims.general_utils import get_DTS
from diyims.ipfs_utils import get_url_dict
from diyims.path_utils import (
    get_path_dict,
    get_unique_item_file,
    get_install_template_dict,
)
from diyims.py_version_dep import get_sql_str
from diyims.want_item_utils import refresh_want_item_dict
from diyims.beacon_runner import run_beacon
from diyims.error_classes import ApplicationNotInstalledError


def create_beacon_CID(logger):
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path, timeout=60)
    conn.row_factory = sqlite3.Row

    header_row = queries.select_last_peer_table_entry_header(conn)

    want_item_dict = refresh_want_item_dict()
    want_item_dict["want_CID"] = header_row["object_CID"]
    want_item_dict["DTS"] = get_DTS()

    conn.close()
    want_item_path = path_dict["want_item_path"]
    proto_item_file = path_dict["want_item_file"]
    want_item_file = get_unique_item_file(want_item_path, proto_item_file)

    with open(want_item_file, "w") as write_file:
        json.dump(want_item_dict, write_file, indent=4)

    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "true", "pin": "false"}
    i = 0
    not_found = True
    while i < 30 and not_found:
        try:
            with requests.Session().post(
                url=url_dict["add"], params=add_params, files=add_files, timeout=30.15
            ) as r:
                r.raise_for_status()
                json_dict = json.loads(r.text)
                last_peer_table_entry_CID = json_dict["Hash"]
                beacon_CID = last_peer_table_entry_CID
                not_found = False
                logger.debug("Create")
        except ConnectionError:
            logger.exception()
            sleep(1)
            i += 1

    return beacon_CID, want_item_file


def non_multi_flash():
    beacon_CID, satisfy_CID = create_beacon_CID()
    satisfy_beacon(satisfy_CID)
    run_beacon(beacon_CID)
    return


def satisfy_beacon(logger, want_item_file):
    url_dict = get_url_dict()
    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "false", "pin": "false"}
    i = 0
    not_found = True
    while i < 30 and not_found:
        try:
            with requests.post(
                url=url_dict["add"], params=add_params, files=add_files
            ) as r:
                r.raise_for_status()
                not_found = False
                logger.debug("Satisfy")
        except ConnectionError:
            logger.exception()
            sleep(1)
            i += 1
    return


def get_beacon_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    beacon_dict = {}
    beacon_dict["minutes_to_run"] = parser["Beacon"]["minutes_to_run"]
    beacon_dict["long_period_seconds"] = parser["Beacon"]["long_period_seconds"]
    beacon_dict["short_period_seconds"] = parser["Beacon"]["short_period_seconds"]
    beacon_dict["number_of_periods"] = parser["Beacon"]["number_of_periods"]

    return beacon_dict


def purge_want_items():  # NOTE: add date attributes to selection for purge
    path_dict = get_path_dict()
    for file in Path(path_dict["want_item_path"]).glob("want_item*.json"):
        Path(file).unlink()
