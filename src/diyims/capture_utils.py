"""
Contains FINDPROVS speculation.

It appears that the output of findprovs  returns an 'ID' value of null for 'Type' 4.
'Type' 4 is one of several records(?) in the routing system.

The ID can be found in 'Responses' which is a dictionary of lists

The routing system has some inertia and retains the node as a provider after the cid is
removed and a garbage collection has run.

"""

import json
import sqlite3
from datetime import datetime, timezone
from sqlite3 import IntegrityError

import requests

# from rich import print
from diyims.database_utils import insert_peer_row, refresh_peer_table_dict
from diyims.ipfs_utils import get_url_dict
from diyims.path_utils import get_path_dict

# from time import sleep


def capture_peer_stats():
    # print(str(datetime.now(timezone.utc)))
    for _ in range(1):
        # print(str(datetime.now(timezone.utc)))
        added_stats = capture_bitswap_peers()
        added_swarm = get_swarm_peers()
        # print(str(datetime.now(timezone.utc)), added_stats, added_swarm)
        # sleep(2)

    return added_stats + added_swarm


def capture_bitswap_peers():
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)

    with requests.post(url_dict["bitswap_stat"], stream=False) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)
        peer_list = json_dict["Peers"]

        found = 0
        added = 0

        for peer in peer_list:
            peer_table_dict = refresh_peer_table_dict()
            DTS = str(datetime.now(timezone.utc))
            peer_table_dict["peer_ID"] = peer
            peer_table_dict["local_update_DTS"] = DTS
            peer_table_dict["processing_status"] = "BP"
            try:
                insert_peer_row(conn, peer_table_dict)
                conn.commit()
                added = added + 1
            except IntegrityError:
                pass
            found = found + 1
    conn.close()
    # print(f"{found} peers found and {added} added")

    return added


def get_swarm_peers():
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)
    with requests.post(url_dict["swarm_peers"], stream=False) as r:
        r.raise_for_status()
        level_zero_dict = json.loads(r.text)
        level_one_list = level_zero_dict["Peers"]
        found = 0
        added = 0
        for peer_dict in level_one_list:
            peer_table_dict = refresh_peer_table_dict()
            DTS = str(datetime.now(timezone.utc))
            peer_table_dict["peer_ID"] = peer_dict["Peer"]
            peer_table_dict["local_update_DTS"] = DTS
            peer_table_dict["processing_status"] = "SP"
            try:
                insert_peer_row(conn, peer_table_dict)
                conn.commit()
                added = added + 1
            except IntegrityError:
                pass
            found = found + 1
    conn.close()
    # print(f"{found} peers found and {added} added")

    return added
