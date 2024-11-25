import json
import sqlite3

import aiosql
import requests
import datetime
from time import sleep
from pathlib import Path

from diyims.ipfs_utils import get_url_dict
from diyims.general_utils import get_DTS
from diyims.py_version_dep import get_sql_str
from diyims.want_item_utils import refresh_want_item_dict
from diyims.path_utils import get_path_dict, get_unique_item_file


# NOTE: beacon purge both ipfs
def create_beacon_CID(logger, beacon_config_dict):
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path, timeout=int(beacon_config_dict["sql_timeout"]))
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
    while i < int(beacon_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url=url_dict["add"],
                params=add_params,
                files=add_files,
            ) as r:
                r.raise_for_status()
                json_dict = json.loads(r.text)
                last_peer_table_entry_CID = json_dict["Hash"]
                beacon_CID = last_peer_table_entry_CID
                not_found = False
                logger.debug(f"Create {beacon_CID}")
                return beacon_CID, want_item_file

        except requests.exceptions.ConnectionError:
            i += 1
            logger.exception(f"Create retry iteration {i}")
            sleep(int(beacon_config_dict["connect_retry_delay"]))
    return


def flash_beacon(logger, beacon_config_dict, beacon_CID):
    url_dict = get_url_dict()
    get_arg = {
        "arg": beacon_CID,
        # "output": str(path_dict['log_path']) + '/' + IPNS_name + '.txt',  # NOTE: Path does not work
    }
    i = 0
    not_found = True
    while i < int(beacon_config_dict["connect_retries"]) and not_found:
        try:
            logger.debug(f"Flash {beacon_CID} on ")
            with requests.Session().post(
                url_dict["get"], params=get_arg, stream=False
            ) as r:
                r.raise_for_status()
                not_found = False
                logger.debug("Flash off")
        except ConnectionError:
            i += 1
            logger.exception(f"Flash retry iteration {i}")
            sleep(int(beacon_config_dict["connect_retry_delay"]))

    return


def satisfy_beacon(logger, satisfy_config_dict, want_item_file):
    url_dict = get_url_dict()
    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "false", "pin": "false"}
    i = 0
    not_found = True
    while i < int(satisfy_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url=url_dict["add"], params=add_params, files=add_files
            ) as r:
                r.raise_for_status()
                not_found = False
                logger.debug(f"Satisfy {want_item_file}")
            #    Path(want_item_file).unlink()
        except ConnectionError:
            i += 1
            logger.exception(f"Satisfy retry iteration {i}")
            sleep(int(satisfy_config_dict["connect_retry_delay"]))

    return


def purge_want_items():
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)

    path_dict = get_path_dict()
    dir_path = Path(path_dict["want_item_path"])
    pattern = "want_item*.*"
    files = dir_path.glob(pattern)

    for file in files:
        modified_time = file.stat().st_mtime
        modified_date = datetime.datetime.fromtimestamp(modified_time)
        if modified_date >= start_date and modified_date <= end_date:
            Path(file).unlink()
    return
