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
