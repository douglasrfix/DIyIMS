import json
import os
import sqlite3

import aiosql
import requests

from diyims.error_classes import UnSupportedIPFSVersionError
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str
from diyims.url_utils import get_url_dict


def purge():
    url_dict = get_url_dict()
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)
    conn.row_factory = sqlite3.Row
    # header_table_dict = get_header_table_dict()
    header_table_rows = queries.select_all_headers(conn)

    for row in header_table_rows:
        # print(f"header_CID '{row['header_CID']}'")
        if row["object_type"] == "IPNS_name":
            print(
                f"IPNS_name '{row['object_CID']}'"
            )  # NOTE: needs a function to name in danger
            header_CID = row["object_CID"]

            ipfs_path = "/ipfs/" + header_CID

            name_publish_arg = {
                "arg": ipfs_path,
                "resolve": "false",
                "lifetime": "10s",
                "ttl": "10s",
                "key": "self",
                "ipns-base": "base36",
            }

            with requests.post(
                url_dict["name_publish"], params=name_publish_arg, stream=False
            ) as r:
                r.raise_for_status()

        elif row["object_CID"] != "null":
            add_params = {"arg": row["object_CID"]}

            with requests.post(
                url_dict["pin_remove"], params=add_params, stream=False
            ) as r:
                r.raise_for_status()

        add_params = {"arg": row["header_CID"]}

        with requests.post(
            url_dict["pin_remove"], params=add_params, stream=False
        ) as r:
            r.raise_for_status()

    conn.close()

    with requests.post(url_dict["run_gc"], stream=False) as r:
        r.raise_for_status()


def test_ipfs_version():
    url_dict = get_url_dict()
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
            "kubo/0.28.0/",
            "kubo/0.29.0/",
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

    return


def force_purge():
    url_dict = get_url_dict()
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
