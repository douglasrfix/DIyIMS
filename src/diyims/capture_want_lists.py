import json
import sqlite3

import aiosql
import requests

# from datetime import datetime, timezone
# from sqlite3 import IntegrityError
from rich import print

from diyims.sql_table_dict import refresh_want_list_table_dict
from diyims.database_operations import insert_want_list_row
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str

# from diyims.sql_table_dict import get_peer_table_dict
from diyims.url_utils import get_url_dict


def get_unprocessed_peers():
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    peers_processed = 0
    total_CIDs_wanted = 0
    with sqlite3.connect(connect_path) as conn:
        conn.row_factory = sqlite3.Row
        with queries.select_unprocessed_peers_cursor(conn) as query_rows:
            for row in query_rows:
                peer_ID = row["peer_ID"]
                CIDs_wanted = get_want_list(conn, peer_ID)
                peers_processed += 1
                total_CIDs_wanted = total_CIDs_wanted + CIDs_wanted
    conn.close()
    print(
        f"{peers_processed} peers processed with {total_CIDs_wanted} total CIDs found"
    )
    return


def get_want_list(conn, peer_ID):
    url_dict = get_url_dict()
    # path_dict = get_path_dict()
    # sql_str = get_sql_str()
    # queries = aiosql.from_str(sql_str, "sqlite3")
    # connect_path = path_dict["db_file"]
    # conn = sqlite3.connect(connect_path)
    key_arg = {"peer": peer_ID}
    with requests.post(url_dict["want_list"], params=key_arg, stream=True) as r:
        r.raise_for_status()
        CIDs_wanted = 0
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                json_dict = json.loads(decoded_line)
                json_string = str(json_dict["Keys"])
                json_string_len = len(json_string)
                python_string = json_string[1 : json_string_len - 1]
                try:
                    json_dict = json.loads(python_string.replace("'", '"'))
                except json.JSONDecodeError:
                    return
                # print(peer_ID)
                # print(json_dict["/"])
                want_list_table_dict = refresh_want_list_table_dict()
                want_list_table_dict["peer_ID"] = peer_ID
                want_list_table_dict["object_CID"] = json_dict["/"]

                insert_want_list_row(conn, want_list_table_dict)
                conn.commit()
                CIDs_wanted += 1
    return CIDs_wanted
