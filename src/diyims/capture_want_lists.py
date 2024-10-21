import json
import sqlite3
from time import sleep

import aiosql
import requests

# from datetime import datetime, timezone
# from sqlite3 import IntegrityError
from rich import print

from diyims.database_utils import (
    insert_want_list_row,
    refresh_peer_table_dict,
    refresh_want_list_table_dict,
)
from diyims.general_utils import get_DTS
from diyims.ipfs_utils import get_url_dict
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str
from diyims.research_utils import get_bitswap_stat


def get_remote_peers():
    for _ in range(1000):
        get_remote_peer()
        sleep(10)

    return


def get_remote_peer():
    get_bitswap_stat()
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    peers_processed = 0
    total_CIDs_wanted = 0
    CIDs_wanted = 0
    with sqlite3.connect(connect_path) as conn:
        conn.row_factory = sqlite3.Row
        with queries.select_remote_peers_cursor(conn) as query_rows:
            for row in query_rows:
                peer_table_dict = refresh_peer_table_dict()
                peer_table_dict["peer_ID"] = row["peer_ID"]
                peer_table_dict["processing_status"] = row["processing_status"]
                CIDs_wanted = get_want_list(conn, peer_table_dict)
                peers_processed += 1
                total_CIDs_wanted = total_CIDs_wanted + CIDs_wanted
    conn.close()
    print(
        f"{peers_processed} peers processed with {total_CIDs_wanted} total CIDs found"
    )
    return


def get_want_list(conn, peer_table_dict):
    """
    given a peerID, bitswap returns a dictionary of lists of a dictionary of lists
    in a single block of text
    """
    url_dict = get_url_dict()
    key_arg = {"peer": peer_table_dict["peer_ID"]}
    with requests.post(url_dict["want_list"], params=key_arg, stream=False) as r:
        r.raise_for_status()
        CID_count = 0
        level_zero_dict = json.loads(r.text)
        level_one_list = level_zero_dict[
            "Keys"
        ]  # this is composed of a dictionary of lists

        if str(level_one_list) != "None":
            for level_two_dict in level_one_list:
                want_item = level_two_dict["/"]
                DTS = get_DTS()
                want_list_table_dict = refresh_want_list_table_dict()
                want_list_table_dict["peer_ID"] = peer_table_dict["peer_ID"]
                want_list_table_dict["object_CID"] = want_item
                want_list_table_dict["insert_DTS"] = DTS
                want_list_table_dict["source_peer_type"] = peer_table_dict[
                    "processing_status"
                ]

                insert_want_list_row(conn, want_list_table_dict)
                conn.commit()
                CID_count += 1

        return CID_count
