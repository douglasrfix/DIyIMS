"""# NOTE:
The beacon length should stand out from regular traffic.(2)
This will be? measured by capturing stats from the swarm (1)
The stats captured will also be used to create timing information (3)
    will be used to load test the system as well as test for beacon distortion.
"""

import json
import sqlite3
import aiosql
import requests
from datetime import datetime, timedelta, date
from time import sleep
from pathlib import Path
from multiprocessing.managers import BaseManager

from diyims.ipfs_utils import get_url_dict
from diyims.general_utils import get_DTS, get_shutdown_target
from diyims.py_version_dep import get_sql_str
from diyims.want_item_utils import refresh_want_item_dict
from diyims.path_utils import get_path_dict, get_unique_item_file
from diyims.config_utils import get_beacon_config_dict, get_satisfy_config_dict
from diyims.logger_utils import get_logger


def beacon_main():
    beacon_config_dict = get_beacon_config_dict()
    logger = get_logger(
        beacon_config_dict["log_file"],
        "none",
    )
    wait_seconds = int(beacon_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Beacon.")
    target_DT = get_shutdown_target(beacon_config_dict)
    purge_want_items()
    logger.info("Purge want item files complete")
    target_DT = get_shutdown_target(beacon_config_dict)
    current_DT = datetime.now()

    max_intervals = int(beacon_config_dict["max_intervals"])
    logger.info(f"Shutdown target {target_DT} or {max_intervals} intervals.")
    beacon_interval = 0
    satisfy_dict = {}

    queue_server = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    queue_server.register("get_satisfy_queue")
    queue_server.register("get_beacon_queue")
    queue_server.connect()
    satisfy_queue = queue_server.get_satisfy_queue()
    beacon_queue = queue_server.get_beacon_queue()
    while target_DT > current_DT and beacon_interval < max_intervals:
        for _ in range(int(beacon_config_dict["number_of_periods"])):
            # NOTE: put process here
            beacon_CID, want_item_file = create_beacon_CID(logger, beacon_config_dict)
            satisfy_dict["status"] = "run"
            satisfy_dict["wait_time"] = beacon_config_dict["short_period_seconds"]
            satisfy_dict["want_item_file"] = want_item_file
            satisfy_queue.put(satisfy_dict)
            message = beacon_queue.get()
            logger.debug(message)

            flash_beacon(logger, beacon_config_dict, beacon_CID)

        for _ in range(int(beacon_config_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger, beacon_config_dict)
            satisfy_dict["status"] = "run"
            satisfy_dict["wait_time"] = beacon_config_dict["long_period_seconds"]
            satisfy_dict["want_item_file"] = want_item_file
            satisfy_queue.put(satisfy_dict)
            message = beacon_queue.get()
            logger.debug(message)

            flash_beacon(logger, beacon_config_dict, beacon_CID)
        beacon_interval += 1
        current_DT = datetime.now()
    satisfy_dict["status"] = "shutdown"
    satisfy_queue.put(satisfy_dict)
    message = beacon_queue.get()
    logger.info(f"Satisfy status {message}")
    logger.info("Normal shutdown of Beacon.")
    return


def create_beacon_CID(logger, beacon_config_dict):
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path, timeout=int(beacon_config_dict["sql_timeout"]))
    conn.row_factory = sqlite3.Row

    header_row = queries.select_last_peer_table_entry_header(
        conn
    )  # NOTE: needs to point to network name

    want_item_dict = refresh_want_item_dict()
    want_item_dict["want_CID"] = header_row["object_CID"]
    want_item_dict["DTS"] = get_DTS()

    conn.close()
    want_item_path = path_dict["want_item_path"]
    proto_item_file = path_dict["want_item_file"]
    want_item_file = get_unique_item_file(want_item_path, proto_item_file)

    with open(want_item_file, "w") as write_file:
        json.dump(want_item_dict, write_file, indent=4)

    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "true", "pin": "false"}
    i = 0
    not_found = True
    while i < int(beacon_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url=url_dict["add"],
                params=add_params,
                files=add_files,
            ) as r:
                r.raise_for_status()
                json_dict = json.loads(r.text)
                last_peer_table_entry_CID = json_dict["Hash"]
                beacon_CID = last_peer_table_entry_CID
                not_found = False
                logger.debug(f"Create {beacon_CID}")
                return beacon_CID, want_item_file

        except requests.exceptions.ConnectionError:
            i += 1
            logger.exception(f"Create retry iteration {i}")
            sleep(int(beacon_config_dict["connect_retry_delay"]))
    return


def flash_beacon(logger, beacon_config_dict, beacon_CID):
    url_dict = get_url_dict()
    get_arg = {
        "arg": beacon_CID,
        # "output": str(path_dict['log_path']) + '/' + IPNS_name + '.txt',  # NOTE: Path does not work
    }
    i = 0
    not_found = True
    while i < int(beacon_config_dict["connect_retries"]) and not_found:
        try:
            logger.debug(f"Flash {beacon_CID} on ")
            with requests.Session().post(
                url_dict["get"], params=get_arg, stream=False
            ) as r:
                r.raise_for_status()
                not_found = False
                logger.debug("Flash off")
        except ConnectionError:
            i += 1
            logger.exception(f"Flash retry iteration {i}")
            sleep(int(beacon_config_dict["connect_retry_delay"]))

    return


def satisfy_main():
    satisfy_config_dict = get_satisfy_config_dict()
    logger = get_logger(
        satisfy_config_dict["log_file"],
        "none",
    )
    wait_seconds = int(satisfy_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Satisfy.")
    logger.info("Shutdown signal comes from Beacon.")

    queue_server = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    queue_server.register("get_satisfy_queue")
    queue_server.register("get_beacon_queue")
    queue_server.connect()
    satisfy_queue = queue_server.get_satisfy_queue()
    beacon_queue = queue_server.get_beacon_queue()
    satisfy_dict = satisfy_queue.get()

    while satisfy_dict["status"] == "run":
        wait_time = int(satisfy_dict["wait_time"])
        want_item_file = satisfy_dict["want_item_file"]
        beacon_queue.put(satisfy_dict["status"])
        sleep(wait_time)
        satisfy_beacon(logger, satisfy_config_dict, want_item_file)
        satisfy_dict = satisfy_queue.get()

    beacon_queue.put(satisfy_dict["status"])
    logger.info("Normal shutdown of Satisfy.")
    return


def satisfy_beacon(logger, satisfy_config_dict, want_item_file):
    url_dict = get_url_dict()
    add_files = {"file": open(want_item_file, "rb")}
    add_params = {"only-hash": "false", "pin": "false"}
    i = 0
    not_found = True
    while i < int(satisfy_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url=url_dict["add"], params=add_params, files=add_files
            ) as r:
                r.raise_for_status()
                not_found = False
                logger.debug(f"Satisfy {want_item_file}")
            #    Path(want_item_file).unlink()
        except ConnectionError:
            i += 1
            logger.exception(f"Satisfy retry iteration {i}")
            sleep(int(satisfy_config_dict["connect_retry_delay"]))

    return


def purge_want_items():
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    path_dict = get_path_dict()
    dir_path = Path(path_dict["want_item_path"])
    pattern = "want_item*.*"
    files = dir_path.glob(pattern)

    for file in files:
        modified_time = file.stat().st_mtime
        modified_date = date.fromtimestamp(modified_time)
        if modified_date >= start_date and modified_date <= end_date:
            Path(file).unlink()  # NOTE: failing, need to delay for >
    return
