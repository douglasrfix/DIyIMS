import json
import sqlite3
from datetime import datetime
from requests.exceptions import ConnectionError
from time import sleep

import aiosql
import requests


from sqlite3 import IntegrityError


from diyims.database_utils import (
    insert_want_list_row,
    select_want_list_entry_by_key,
    update_last_update_DTS,
    refresh_peer_table_dict,
    refresh_want_list_table_dict,
)
from diyims.general_utils import get_DTS, get_shutdown_target
from diyims.ipfs_utils import get_url_dict, wait_on_ipfs
from diyims.path_utils import get_path_dict
from diyims.py_version_dep import get_sql_str
from diyims.logger_utils import get_logger
from diyims.config_utils import get_want_list_config_dict


def capture_peer_want_lists(runtime_peer_type):
    want_list_config_dict = get_want_list_config_dict()
    logger = get_logger(want_list_config_dict["log_file"])
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    wait_seconds = int(want_list_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Want List Capture.")
    target_DT = get_shutdown_target(want_list_config_dict)
    current_DT = datetime.now()
    max_intervals = int(want_list_config_dict["max_intervals"])
    number_of_samples = int(want_list_config_dict["number_of_samples"])
    seconds_per_sample = 60 // int(want_list_config_dict["samples_per_minute"])
    total_seconds = number_of_samples * seconds_per_sample
    logger.info(
        f"Shutdown target {target_DT} or {max_intervals} intervals of {total_seconds} seconds."
    )
    provider_interval = 0
    total_peers_processed = 0
    total_CIDs_captured = 0

    while target_DT > current_DT and provider_interval < max_intervals:
        i = 0
        while i < number_of_samples:
            peers_processed, total_CIDs_wanted = capture_want_lists_for_peers(
                logger, want_list_config_dict, runtime_peer_type
            )
            total_peers_processed = total_peers_processed + peers_processed
            total_CIDs_captured = total_CIDs_captured + total_CIDs_wanted
            wait_seconds = seconds_per_sample
            i += 1
            sleep(wait_seconds)

        log_string = f"{total_peers_processed} NP peers processed with {total_CIDs_wanted} CIDs found."
        logger.debug(log_string)
        provider_interval += 1
        current_DT = datetime.now()

    logger.info("Normal shutdown of Want List Capture.")
    return


def capture_want_lists_for_peers(logger, want_list_config_dict, runtime_peer_type):
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    connect_path = path_dict["db_file"]
    peers_processed = 0
    total_CIDs_wanted = 0
    CIDs_wanted = 0
    queries = aiosql.from_str(sql_str, "sqlite3")
    with sqlite3.connect(
        connect_path, timeout=int(want_list_config_dict["sql_timeout"])
    ) as conn:
        conn.row_factory = sqlite3.Row
        with queries.select_all_providers_cursor(
            conn, runtime_peer_type
        ) as rows_of_peers:
            for peer in rows_of_peers:
                peer_table_dict = refresh_peer_table_dict()
                peer_table_dict["peer_ID"] = peer["peer_ID"]
                peer_table_dict["processing_status"] = peer["processing_status"]
                CIDs_wanted = capture_peer_want_list_by_id(
                    logger, want_list_config_dict, conn, queries, peer_table_dict
                )
                peers_processed += 1
                total_CIDs_wanted = total_CIDs_wanted + CIDs_wanted
    conn.close()
    log_string = (
        f"{peers_processed} peers processed with {total_CIDs_wanted} CIDs found."
    )
    logger.debug(log_string)
    return peers_processed, total_CIDs_wanted


def capture_peer_want_list_by_id(
    logger, want_list_config_dict, conn, queries, peer_table_dict
):
    url_dict = get_url_dict()
    key_arg = {"peer": peer_table_dict["peer_ID"]}
    i = 0
    not_found = True
    CID_count = 0
    while i < int(want_list_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url_dict["want_list"], params=key_arg, stream=False
            ) as r:
                r.raise_for_status()

                level_zero_dict = json.loads(r.text)
                CID_count = CID_count + decode_want_list_structure(
                    conn, queries, peer_table_dict, level_zero_dict
                )
                not_found = False
        except ConnectionError:
            i = +1
            logger.exception(f"Satisfy retry iteration {i}")
            sleep(int(want_list_config_dict["connect_retry_delay"]))

    return CID_count


def decode_want_list_structure(conn, queries, peer_table_dict, level_zero_dict):
    """
    given a peerID, bitswap returns a dictionary of lists of a dictionary of lists
    in a single block of text
    """

    CID_count = 0
    level_one_list = level_zero_dict[
        "Keys"
    ]  # this is composed of a dictionary of lists

    if str(level_one_list) != "None":
        for level_two_dict in level_one_list:
            want_item = level_two_dict["/"]
            DTS = get_DTS()
            want_list_table_dict = refresh_want_list_table_dict()
            want_list_table_dict["peer_ID"] = peer_table_dict["peer_ID"]
            want_list_table_dict["object_CID"] = want_item
            want_list_table_dict["insert_DTS"] = DTS
            want_list_table_dict["last_update_DTS"] = DTS
            want_list_table_dict["source_peer_type"] = peer_table_dict["peer_type"]

            try:
                insert_want_list_row(conn, queries, want_list_table_dict)
            except IntegrityError:
                want_list_entry = select_want_list_entry_by_key(
                    conn, queries, want_list_table_dict
                )
                insert_dt = datetime.fromisoformat(want_list_entry["insert_DTS"])
                update_dt = datetime.fromisoformat(
                    want_list_table_dict["last_update_DTS"]
                )
                delta = update_dt - insert_dt
                want_list_table_dict["insert_update_delta"] = int(delta.total_seconds())
                update_last_update_DTS(conn, queries, want_list_table_dict)

            conn.commit()
            CID_count = 1

    return CID_count


if __name__ == "__main__":
    capture_peer_want_lists("NP")
