import sqlite3
from datetime import datetime, timezone
from dateutil.parser import parse

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


def get_DTS():  # NOTE: rename to dts utc
    DTS = str(datetime.now(timezone.utc))

    return DTS


def get_shutdown_target(config_dict):
    current_date = datetime.today()
    shutdown_time = config_dict["shutdown_time"]
    target_DT = parse(shutdown_time, default=current_date)

    return target_DT
