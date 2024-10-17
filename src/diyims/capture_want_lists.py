import json
import sqlite3

import aiosql
import requests

# from datetime import datetime, timezone
# from sqlite3 import IntegrityError
from rich import print

# from diyims.general_utils import insert_peer_row
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str

# from diyims.sql_table_dict import get_peer_table_dict
from diyims.url_utils import get_url_dict


def get_unprocessed_peers():
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    with sqlite3.connect(connect_path) as conn:
        conn.row_factory = sqlite3.Row
        with queries.select_unprocessed_peers_cursor(conn) as query_rows:
            for row in query_rows:
                peer_ID = row["peer_ID"]
                get_want_list(peer_ID)
    conn.close()
    return


def get_want_list(peer_ID):
    url_dict = get_url_dict()
    key_arg = {"peer": peer_ID}
    with requests.post(url_dict["want_list"], params=key_arg, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                json_dict = json.loads(decoded_line)
                json_string = str(json_dict["Keys"])
                json_string_len = len(json_string)
                python_string = json_string[1 : json_string_len - 1]
                try:
                    python_dict = json.loads(python_string.replace("'", '"'))
                except json.JSONDecodeError:
                    return

                print(python_dict["/"])

        return

        """
        peer_table_dict = get_peer_table_dict()
        peer_table_dict["peer_ID"] = python_dict["ID"]
        try:
        insert_peer_row(peer_table_dict)
        count = count + 1
        except IntegrityError:
        pass
        print(count)
        # print(provider_dict)
        """
