# FIXME: fix references to cartest .car file
# FIXME: set hash only to false and pin to true
import json
import sqlite3
from datetime import datetime, timezone
from importlib import resources
from sqlite3 import Error

import aiosql
import requests
from rich import print

from diyims.paths import get_path_dict
from diyims.urls import get_url_dict
from diyims.error_classes import UnTestedPlatformError


def create():
    try:
        path_dict = get_path_dict()

    except UnTestedPlatformError:
        pass

    sql_str = resources.read_text(
        "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
    )
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_path"]
    conn = sqlite3.connect(connect_path)

    try:
        queries.create_schema(conn)
        print("DB Schema creation successful.")
    except Error as e:
        print(f"The error '{e}' occurred.")

    conn.close()


def init():
    try:
        path_dict = get_path_dict()

    except UnTestedPlatformError:
        pass

    url_dict = get_url_dict()
    sql_str = resources.read_text(
        "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
    )
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_path"]
    conn = sqlite3.connect(connect_path)

    peer_table_dict = {}
    peer_table_dict["version"] = "0"
    peer_table_dict["peer_id"] = "null"
    peer_table_dict["IPNS_name"] = "null"

    """
    Create anchor entry of the linked list.
    It is created so that the entries pointing to real objects have a prior CID
    """

    """
    DTS is the same for all artifacts of this transaction
    """
    DTS = str(datetime.now(timezone.utc))

    print("This process can take several minutes. Have a cup of coffee.")
    object_CID = "null"
    object_type = "linked_list_header"
    header_CID, IPNS_name = ipfs_header_create(DTS, object_CID, object_type)

    print(f"First header CID (head of chain) '{header_CID}'")
    print("Published first header")

    """

    Create the initial peer table entry for this peer.
    """

    DTS = str(datetime.now(timezone.utc))

    with requests.post(url_dict["id"], stream=False) as r:
        json_dict = json.loads(r.text)

    peer_table_dict["version"] = "0"
    peer_table_dict["peer_id"] = json_dict["ID"]
    peer_table_dict["IPNS_name"] = IPNS_name

    peer_path = path_dict["peer_path"]
    add_params = {"only-hash": "true", "pin": "false"}

    with open(peer_path, "w") as write_file:
        json.dump(peer_table_dict, write_file, indent=4)

    add_files = {"file": open(peer_path, "rb")}

    with requests.post(url=url_dict["add"], params=add_params, files=add_files) as r:
        json_dict = json.loads(r.text)

    object_CID = json_dict["Hash"]
    object_type = "peer_table_entry"
    header_CID, IPNS_name = ipfs_header_create(DTS, object_CID, object_type)

    print(f"Second header CID '{header_CID}'")
    print("Published second header")

    print(f"First network peer entry CID '{object_CID}'")

    queries.insert_peer_row(
        conn,
        peer_table_dict["version"],
        peer_table_dict["peer_id"],
        peer_table_dict["IPNS_name"],
    )
    queries.commit(conn)
    conn.close()

    network_name = import_car()
    print(network_name)


def ipfs_header_create(DTS, object_CID, object_type):
    try:
        path_dict = get_path_dict()

    except UnTestedPlatformError:
        pass

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
    add_params = {"only-hash": "true", "pin": "false"}

    with open(header_json_path, "w") as write_file:
        json.dump(header_dict, write_file, indent=4)

    add_files = {"file": open(header_json_path, "rb")}

    with requests.post(url=url_dict["add"], params=add_params, files=add_files) as r:
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


def import_car():
    url_dict = get_url_dict()

    dag_import_files = {
        "file": resources.open_binary("diyims.resources", "cartest.car")
    }
    dag_import_params = {
        "pin-roots": "true",
        "silent": "false",
        "stats": "false",
        "allow-big-block": "false",
    }

    with requests.post(
        url=url_dict["dag_import"], params=dag_import_params, files=dag_import_files
    ) as r:
        json_dict = json.loads(r.text)
        imported_CID = json_dict["Root"]["Cid"]["/"]

    return imported_CID
