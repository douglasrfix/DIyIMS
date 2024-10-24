import json
import sqlite3
from pathlib import Path

import aiosql
import requests

from diyims.general_utils import get_DTS
from diyims.ipfs_utils import get_url_dict
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str
from diyims.want_item_utils import refresh_want_item_dict


def create_beacon_CID():
    url_dict = get_url_dict()
    path_dict = get_path_dict()
    want_item_path = path_dict["header_path"]  # NOTE: create config entry for want item
    want_item_file = Path(want_item_path).joinpath("want_item.json")  #

    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)
    conn.row_factory = sqlite3.Row

    header_row = queries.select_last_peer_table_entry_header(conn)

    want_item_dict = refresh_want_item_dict()
    want_item_dict["want_CID"] = header_row["object_CID"]
    want_item_dict["DTS"] = get_DTS()

    conn.close()

    with open(want_item_file, "w") as write_file:  # NOTE:make unique file name
        json.dump(want_item_dict, write_file, indent=4)

    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "true", "pin": "false"}
    with requests.post(url=url_dict["add"], params=add_params, files=add_files) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)
        last_peer_table_entry_CID = json_dict["Hash"]

    return last_peer_table_entry_CID, want_item_file


def flash_beacon(beacon_CID):
    url_dict = get_url_dict()
    get_arg = {
        "arg": beacon_CID,
        # "output": str(path_dict['log_path']) + '/' + IPNS_name + '.txt',  # NOTE: Path does not work
    }

    with requests.post(url_dict["get"], params=get_arg, stream=False) as r:
        r.raise_for_status()

    return


def satisfy_beacon(want_item_file):
    url_dict = get_url_dict()
    path_dict = get_path_dict()
    want_item_path = path_dict[
        "header_path"
    ]  # NOTE: create config entry for want items
    want_item_file = Path(want_item_path).joinpath("want_item.json")  #

    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "false", "pin": "false"}
    with requests.post(url=url_dict["add"], params=add_params, files=add_files) as r:
        r.raise_for_status()

    return
