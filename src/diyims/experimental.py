import json

# import sqlite3

import requests

# import aiosql

from diyims.urls import get_url_dict

# from diyims.import_lib import get_sql_str
# from diyims.paths import get_path_dict


def test():
    url_dict = get_url_dict()
    # path_dict = get_path_dict()
    with requests.post(url_dict["pin_list"], stream=False) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)

        try:
            for key in json_dict["Keys"]:
                add_params = {"arg": key}

                with requests.post(
                    url_dict["pin_remove"], params=add_params, stream=False
                ) as r:
                    r.raise_for_status()

        except KeyError:
            pass

    with requests.post(url_dict["run_gc"], stream=False) as r:
        r.raise_for_status()


"""
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_path"]
    conn = sqlite3.connect(connect_path)
    network_table_dict = {}
    network_table_dict["version"] = "0"
    network_table_dict["network_name"] = "null"
    network_name = queries.select_network_name(conn)

    if network_name is not None:

        conn.close()
"""
