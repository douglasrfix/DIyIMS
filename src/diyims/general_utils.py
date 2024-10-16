import sqlite3

import aiosql

from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str


def get_network_name():
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)
    conn.row_factory = sqlite3.Row
    query_row = queries.select_network_name(conn)
    network_name = query_row["network_name"]
    conn.close()
    return network_name


def insert_peer_row(peer_table_dict):
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)

    queries.insert_peer_row(
        conn,
        peer_table_dict["version"],
        peer_table_dict["peer_id"],
        peer_table_dict["update_seq"],
        peer_table_dict["IPNS_name"],
        peer_table_dict["update_dts"],
        peer_table_dict["platform"],
        peer_table_dict["python_version"],
        peer_table_dict["ipfs_agent"],
    )
    queries.commit(conn)
    conn.close()

    return
