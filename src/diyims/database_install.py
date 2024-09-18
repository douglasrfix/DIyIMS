import json
import os
import sqlite3
from datetime import datetime, timezone
from importlib import resources
from sqlite3 import Error

import aiosql
import requests
from rich import print

from diyims.error_classes import (
    CreateSchemaError,
    UnSupportedIPFSVersionError,
    PreExistingInstallationError,
    UnTestedPlatformError,
)
from diyims.header_ops import ipfs_header_create
from diyims.paths import get_path_dict
from diyims.urls import get_url_dict


def create():
    try:
        path_dict = get_path_dict()

    except UnTestedPlatformError as error:
        path_dict = error.dict

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
        conn.close()
        raise (CreateSchemaError(e))


def init():
    try:
        path_dict = get_path_dict()

    except UnTestedPlatformError as error:
        path_dict = error.dict

    network_table_dict = {}
    network_table_dict["version"] = "0"
    network_table_dict["network_name"] = "null"
    url_dict = get_url_dict()

    sql_str = resources.read_text(
        "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
    )
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_path"]
    conn = sqlite3.connect(connect_path)
    network_name = queries.select_network_name(conn)

    if network_name is not None:
        conn.close()
        raise (PreExistingInstallationError(""))

    conn.close()
    conn = sqlite3.connect(connect_path)
    conn.row_factory = sqlite3.Row

    with requests.post(url_dict["id"], stream=False) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)

        supported_agents = [
            "kubo/0.22.0/",
            "kubo/0.23.0/",
            "kubo/0.24.0/",
            "kubo/0.25.0/",
            "kubo/0.26.0/",
            "kubo/0.27.0/",
        ]
        match_count = 0
        for x in supported_agents:
            if json_dict["AgentVersion"] not in x:
                pass
            else:
                match_count = match_count + 1

        try:
            match_count = int(os.environ["OVERRIDE_IPFS_VERSION"])

        except KeyError:
            pass

        if match_count == 0:
            raise (UnSupportedIPFSVersionError(json_dict["AgentVersion"]))

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
        r.raise_for_status()
        json_dict = json.loads(r.text)

    peer_table_dict["version"] = "0"
    peer_table_dict["peer_id"] = json_dict["ID"]
    peer_table_dict["IPNS_name"] = IPNS_name

    peer_path = path_dict["peer_path"]
    add_params = {"only-hash": "false", "pin": "true"}

    with open(peer_path, "w") as write_file:
        json.dump(peer_table_dict, write_file, indent=4)

    add_files = {"file": open(peer_path, "rb")}

    with requests.post(url=url_dict["add"], params=add_params, files=add_files) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)

    object_CID = json_dict["Hash"]
    object_type = "peer_table_entry"
    header_CID, IPNS_name = ipfs_header_create(DTS, object_CID, object_type)

    print(f"Second header CID '{header_CID}'")
    print("Published second header")

    print(f"First network peer entry CID '{object_CID}'")

    network_table_dict["network_name"] = import_car()
    print(network_table_dict["network_name"])

    queries.insert_peer_row(
        conn,
        peer_table_dict["version"],
        peer_table_dict["peer_id"],
        peer_table_dict["IPNS_name"],
    )
    queries.commit(conn)
    queries.insert_network_row(
        conn,
        network_table_dict["version"],
        network_table_dict["network_name"],
    )
    queries.commit(conn)
    conn.close()


def import_car():
    url_dict = get_url_dict()

    dag_import_files = {"file": resources.open_binary("diyims.resources", "cartxt.car")}
    dag_import_params = {
        "pin-roots": "true",
        "silent": "false",
        "stats": "false",
        "allow-big-block": "false",
    }

    with requests.post(
        url=url_dict["dag_import"], params=dag_import_params, files=dag_import_files
    ) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)
        imported_CID = json_dict["Root"]["Cid"]["/"]

    return imported_CID
