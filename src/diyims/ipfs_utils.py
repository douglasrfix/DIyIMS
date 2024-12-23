import json
import os
import sqlite3
from time import sleep

import aiosql
import requests
from requests.exceptions import HTTPError

from diyims.error_classes import UnSupportedIPFSVersionError
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str, get_car_path
from diyims.database_utils import refresh_network_table_dict, select_network_name


def get_url_dict():
    url_dict = {}
    url_dict["add"] = "http://127.0.0.1:5001/api/v0/add"
    url_dict["get"] = "http://127.0.0.1:5001/api/v0/get"
    url_dict["id"] = "http://127.0.0.1:5001/api/v0/id"
    url_dict["dag_import"] = "http://127.0.0.1:5001/api/v0/dag/import"
    url_dict["name_publish"] = "http://127.0.0.1:5001/api/v0/name/publish"
    url_dict["find_providers"] = "http://127.0.0.1:5001/api/v0/routing/findprovs"
    url_dict["pin_list"] = "http://127.0.0.1:5001/api/v0/pin/ls"
    url_dict["pin_add"] = "http://127.0.0.1:5001/api/v0/pin/add"
    url_dict["pin_remove"] = "http://127.0.0.1:5001/api/v0/pin/rm"
    url_dict["run_gc"] = "http://127.0.0.1:5001/api/v0/repo/gc"
    url_dict["want_list"] = "http://127.0.0.1:5001/api/v0/bitswap/wantlist"
    url_dict["bitswap_stat"] = (
        "http://127.0.0.1:5001/api/v0/bitswap/stat"  # NOTE: make the key the name of the command
    )
    url_dict["swarm_peers"] = "http://127.0.0.1:5001/api/v0/swarm/peers"

    return url_dict


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
            "kubo/0.32.1/",
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

    return json_dict["AgentVersion"]


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


def wait_on_ipfs(logger):
    url_dict = get_url_dict()
    from diyims.config_utils import get_ipfs_config_dict

    ipfs_config_dict = get_ipfs_config_dict()
    i = 0
    not_found = True
    logger.debug("ipfs wait started.")
    sleep(int(ipfs_config_dict["connect_retry_delay"]))
    while i < 30 and not_found:
        try:
            with requests.post(url=url_dict["id"]) as r:
                r.raise_for_status()
                not_found = False
                logger.debug("ipfs wait completed.")
        except requests.exceptions.ConnectionError:
            i += 1
            logger.exception(f"wait on ipfs iteration {i}.")
            sleep(int(ipfs_config_dict["connect_retry_delay"]))

    return


def reset_network_name():
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)
    conn.row_factory = sqlite3.Row
    url_dict = get_url_dict()
    network_table_dict = refresh_network_table_dict()
    network_table_dict = select_network_name(conn, queries, network_table_dict)
    add_params = {"arg": network_table_dict["network_name"]}
    print(add_params)
    try:
        with requests.post(
            url_dict["pin_remove"], params=add_params, stream=False
        ) as r:
            r.raise_for_status()
    except HTTPError:
        pass

    print(r)
    print("pin remove")

    with requests.post(url_dict["run_gc"], stream=False) as r:
        r.raise_for_status()
    print(r)
    print("run gc")

    car_path = get_car_path()
    dag_import_files = {"file": car_path}
    dag_import_params = {
        "pin-roots": "true",  # http status 500 if false but true does not pin given not in off-line mode
        "silent": "false",
        "stats": "false",
        "allow-big-block": "false",
    }

    with requests.post(
        url=url_dict["dag_import"], params=dag_import_params, files=dag_import_files
    ) as r:
        r.raise_for_status()
    print(r)
    print("import dag")

    """
    json_dict = json.loads(r.text)
    imported_CID = json_dict["Root"]["Cid"]["/"]

        # import does not pin unless in offline mode so it must be done manually
    pin_add_params = {"arg": imported_CID}
    with requests.post(
            url_dict["pin_add"], params=pin_add_params, stream=False
        ) as r:
        r.raise_for_status()
    print(r)
    print("add pin")
    """
    return


if __name__ == "__main__":
    reset_network_name()
