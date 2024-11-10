import json
import sqlite3
from datetime import datetime
from time import sleep

import aiosql
import requests

# from datetime import datetime, timezone
from sqlite3 import IntegrityError
from rich import print

from diyims.database_utils import (
    insert_want_list_row,
    select_want_list_entry_by_key,
    update_last_update_DTS,
    refresh_peer_table_dict,
    refresh_want_list_table_dict,
)
from diyims.general_utils import get_DTS
from diyims.ipfs_utils import get_url_dict
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str

from diyims.research_utils import capture_peer_stats


def process_peers(ten_second_intervals):
    total_peers_captured = 0
    total_peers_processed = 0
    total_CIDs_captured = 0
    for _ in range(ten_second_intervals):
        total_peers_captured = total_peers_captured + capture_peer_stats()
        peers_processed, total_CIDs_wanted = capture_want_list_for_selected_peers()
        total_peers_processed = total_peers_processed + peers_processed
        total_CIDs_captured = total_CIDs_captured + total_CIDs_wanted

    DTS = get_DTS()
    sleep(5)  # sample frequency
    print(
        f"{total_peers_captured} peers captured {total_peers_processed} peers processed with {total_CIDs_captured} total CIDs found at {DTS}"
    )
    return


def capture_want_list_for_selected_peers():
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    connect_path = path_dict["db_file"]
    peers_processed = 0
    total_CIDs_wanted = 0
    CIDs_wanted = 0
    queries = aiosql.from_str(sql_str, "sqlite3")
    with sqlite3.connect(connect_path) as conn:
        conn.row_factory = sqlite3.Row
        with queries.select_all_peers_cursor(conn) as rows_of_peers:
            for peer in rows_of_peers:
                peer_table_dict = refresh_peer_table_dict()
                peer_table_dict["peer_ID"] = peer["peer_ID"]
                peer_table_dict["processing_status"] = peer["processing_status"]
                CIDs_wanted = capture_peer_want_list(conn, queries, peer_table_dict)
                peers_processed += 1
                total_CIDs_wanted = total_CIDs_wanted + CIDs_wanted
    conn.close()
    # print(
    #    f"{peers_processed} peers processed with {total_CIDs_wanted} total CIDs found"
    # )
    return peers_processed, total_CIDs_wanted


def capture_peer_want_list(conn, queries, peer_table_dict):
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
                want_list_table_dict["last_update_DTS"] = DTS
                want_list_table_dict["source_peer_type"] = peer_table_dict[
                    "processing_status"
                ]

                try:
                    insert_want_list_row(conn, queries, want_list_table_dict)
                except IntegrityError:
                    want_list_entry = select_want_list_entry_by_key(
                        conn, queries, want_list_table_dict
                    )
                    insert_dt = datetime.fromisoformat(want_list_entry["insert_DTS"])
                    update_dt = datetime.fromisoformat(
                        want_list_entry["last_update_DTS"]
                    )
                    delta = update_dt - insert_dt
                    want_list_table_dict["insert_update_delta"] = delta.seconds
                    want_list_table_dict["last_update_DTS"] = DTS
                    update_last_update_DTS(conn, queries, want_list_table_dict)

                conn.commit()
                CID_count += 1

    return CID_count
