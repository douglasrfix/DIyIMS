import json
import sqlite3
from importlib import resources

import aiosql
import requests

from diyims.error_classes import UnTestedPlatformError
from diyims.paths import get_path_dict
from diyims.urls import get_url_dict


def ipfs_header_create(DTS, object_CID, object_type):
    try:
        path_dict = get_path_dict()

    except UnTestedPlatformError as error:
        path_dict = error.dict

    url_dict = get_url_dict()

    sql_str = resources.read_text(
        "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
    )
    connect_path = path_dict["db_path"]
    header_conn = sqlite3.connect(connect_path)
    header_conn.row_factory = sqlite3.Row
    queries = aiosql.from_str(sql_str, "sqlite3")
    query_row = queries.select_last_header(header_conn)

    if query_row is None:
        header_dict = {}
        header_dict["version"] = "0"
        header_dict["object_CID"] = object_CID
        header_dict["object_type"] = object_type
        header_dict["insert_DTS"] = DTS
        header_dict["prior_header_CID"] = "null"

        header_CID = "null"

    else:
        header_dict = {}
        header_dict["version"] = "0"
        header_dict["object_CID"] = object_CID
        header_dict["object_type"] = object_type
        header_dict["insert_DTS"] = DTS
        header_dict["prior_header_CID"] = query_row["header_CID"]

        header_CID = "null"

    header_json_path = path_dict["header_path"]
    add_params = {"only-hash": "false", "pin": "true"}

    with open(header_json_path, "w") as write_file:
        json.dump(header_dict, write_file, indent=4)

    add_files = {"file": open(header_json_path, "rb")}

    with requests.post(url=url_dict["add"], params=add_params, files=add_files) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)
        header_CID = json_dict["Hash"]

    ipfs_path = "/ipfs/" + header_CID

    name_publish_arg = {
        "arg": ipfs_path,
        "resolve": "false",
        "lifetime": "24h",
        "key": "self",
        "ipns-base": "base36",
    }

    with requests.post(
        url_dict["name_publish"], params=name_publish_arg, stream=False
    ) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)
        IPNS_name = json_dict["Name"]

    queries.insert_header_row(
        header_conn,
        header_dict["version"],
        header_dict["object_CID"],
        header_dict["object_type"],
        header_dict["insert_DTS"],
        header_dict["prior_header_CID"],
        header_CID,
    )
    queries.commit(header_conn)

    header_conn.close()

    return (header_CID, IPNS_name)
