"""
Contains early kubo 0.22.0 FINDPROVS speculation.

It appears that the output of findprovs  returns an 'ID' value of null for 'Type' 4.
'Type' 4 is one of several records(?) in the routing system.

The ID can be found in 'Responses'

The content of 'Responses' is not JSON. Perhaps list of list? You have to trim the brackets and replace single
quotes with double quotes. This was sufficient for my needs but YMMV.

This appears to yield the same results as the CLI

The routing system has some inertia and retains the node as a provider after the cid is
removed i.e. unpinned and a garbage collection has run.

"""

import json
import sqlite3
import requests
from datetime import datetime, timezone
from sqlite3 import IntegrityError
from time import sleep

from diyims.ipfs_utils import get_url_dict, wait_on_ipfs
from diyims.path_utils import get_path_dict
from diyims.database_utils import insert_peer_row, refresh_peer_table_dict
from diyims.general_utils import get_network_name, get_shutdown_target
from diyims.logger_utils import get_logger
from diyims.config_utils import (
    get_capture_providers_config_dict,
    get_capture_bitswap_config_dict,
    get_capture_swarm_config_dict,
)


def capture_providers_main():
    capture_providers_config_dict = get_capture_providers_config_dict()
    logger = get_logger(capture_providers_config_dict["log_file"])
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    wait_seconds = int(capture_providers_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Peer Capture.")
    target_DT = get_shutdown_target(capture_providers_config_dict)
    current_DT = datetime.now()
    max_intervals = int(capture_providers_config_dict["max_intervals"])
    logger.info(f"Shutdown target {target_DT} or {max_intervals} intervals.")
    capture_providers_interval = 0
    while target_DT > current_DT and capture_providers_interval < max_intervals:
        sleep(int(capture_providers_config_dict["capture_interval_delay"]))

        capture_providers(logger, capture_providers_config_dict)

        current_DT = datetime.now()
        capture_providers_interval += 1

    logger.info("Normal shutdown of Peer Capture.")
    return


def capture_providers(logger, capture_providers_config_dict):
    logger.debug("Startup of Provider Capture.")
    url_dict = get_url_dict()
    path_dict = get_path_dict()
    network_name = get_network_name()
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(
        connect_path, timeout=int(capture_providers_config_dict["sql_timeout"])
    )
    key_arg = {"arg": network_name}
    i = 0
    not_found = True
    while i < int(capture_providers_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url_dict["find_providers"], params=key_arg, stream=True
            ) as r:
                r.raise_for_status()
                not_found = False

                decode_findprovs_structure(logger, conn, r)

        except ConnectionError:
            logger.exception()
            sleep(int(capture_providers_config_dict["connect_retry_delay"]))
            i += 1
    logger.debug("Provider Capture complete.")
    return


def decode_findprovs_structure(logger, conn, r):
    found = 0
    added = 0
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            line_dict = json.loads(decoded_line)
            if line_dict["Type"] == 4:
                responses_string = str(line_dict["Responses"])
                responses_string_len = len(responses_string)
                trimmed_responses_string = responses_string[
                    1 : responses_string_len - 1
                ]
                responses_dict = json.loads(trimmed_responses_string.replace("'", '"'))

                peer_table_dict = refresh_peer_table_dict()
                DTS = str(datetime.now(timezone.utc))
                peer_table_dict["peer_ID"] = responses_dict["ID"]
                peer_table_dict["local_update_DTS"] = DTS
                peer_table_dict["peer_type"] = "NP"
                try:
                    insert_peer_row(conn, peer_table_dict)
                    conn.commit()
                    added = added + 1
                except IntegrityError:
                    pass
                found = found + 1

    conn.close()
    log_string = f"{found} providers found and {added} providers added to peer table"
    logger.debug(log_string)
    return


def capture_bitswap_main():
    capture_bitswap_config_dict = get_capture_bitswap_config_dict()
    logger = get_logger(capture_bitswap_config_dict["log_file"])
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    wait_seconds = int(capture_bitswap_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Capture Bitswap.")

    target_DT = get_shutdown_target(capture_bitswap_config_dict)
    current_DT = datetime.now()
    max_intervals = int(capture_bitswap_config_dict["max_intervals"])
    logger.info(f"Shutdown target {target_DT} or {max_intervals} intervals.")
    capture_bitswap_interval = 0
    while target_DT > current_DT and capture_bitswap_interval < max_intervals:
        sleep(int(capture_bitswap_config_dict["capture_interval_delay"]))
        capture_bitswap_peers(logger, capture_bitswap_config_dict)
        capture_bitswap_interval += 1
        current_DT = datetime.now()

    logger.info("Normal shutdown of Capture Bitswap.")
    return


def capture_bitswap_peers(logger, capture_bitswap_config_dict):
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(
        connect_path, timeout=int(capture_bitswap_config_dict["sql_timeout"])
    )

    i = 0
    not_found = True
    while i < int(capture_bitswap_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(url_dict["bitswap_stat"], stream=False) as r:
                r.raise_for_status()

            not_found = False
            found, added = decode_bitswap_stat_structure(conn, r)
        except ConnectionError:
            logger.exception()
            sleep(int(capture_bitswap_config_dict["connect_retry_delay"]))
            i += 1

    conn.close()
    log_string = (
        f"{found} bitswap peers found and {added} bitswap peers added to peer table"
    )
    logger.info(log_string)
    logger.info("Capture Bitswap complete.")

    return


def decode_bitswap_stat_structure(conn, r):
    found = 0
    added = 0
    json_dict = json.loads(r.text)
    peer_list = json_dict["Peers"]
    for peer in peer_list:
        peer_table_dict = refresh_peer_table_dict()
        DTS = str(datetime.now(timezone.utc))
        peer_table_dict["peer_ID"] = peer
        peer_table_dict["local_update_DTS"] = DTS
        peer_table_dict["peer_type"] = "BP"
        try:
            insert_peer_row(conn, peer_table_dict)
            conn.commit()
            added = added + 1
        except IntegrityError:
            pass
        found = found + 1

    return found, added


def capture_swarm_main():
    capture_swarm_config_dict = get_capture_swarm_config_dict()
    logger = get_logger(capture_swarm_config_dict["log_file"])
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    wait_seconds = int(capture_swarm_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Capture Swarm.")

    target_DT = get_shutdown_target(capture_swarm_config_dict)
    current_DT = datetime.now()
    max_intervals = int(capture_swarm_config_dict["max_intervals"])
    logger.info(f"Shutdown target {target_DT} or {max_intervals} intervals.")
    capture_swarm_interval = 0
    while target_DT > current_DT and capture_swarm_interval < max_intervals:
        sleep(int(capture_swarm_config_dict["capture_interval_delay"]))
        capture_swarm_peers(logger, capture_swarm_config_dict)
        capture_swarm_interval += 1
        current_DT = datetime.now()

    logger.info("Normal shutdown of Capture Swarm.")
    return


def capture_swarm_peers(logger, capture_swarm_config_dict):
    url_dict = get_url_dict()
    path_dict = get_path_dict()

    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(
        connect_path, timeout=int(capture_swarm_config_dict["sql_timeout"])
    )
    i = 0
    not_found = True
    while i < int(capture_swarm_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(url_dict["swarm_peers"], stream=False) as r:
                r.raise_for_status()
            not_found = False
            found, added = decode_swarm_structure(conn, r)
        except ConnectionError:
            logger.exception()
            sleep(int(capture_swarm_config_dict["connect_retry_delay"]))
            i += 1
    conn.close()
    log_string = (
        f"{found} swarm peers found and {added} swarm peers added to peer table"
    )
    logger.info(log_string)
    logger.info("Capture Swarm complete.")

    return


def decode_swarm_structure(conn, r):
    level_zero_dict = json.loads(r.text)
    level_one_list = level_zero_dict["Peers"]
    found = 0
    added = 0
    for peer_dict in level_one_list:
        peer_table_dict = refresh_peer_table_dict()
        DTS = str(datetime.now(timezone.utc))
        peer_table_dict["peer_ID"] = peer_dict["Peer"]
        peer_table_dict["local_update_DTS"] = DTS
        peer_table_dict["peer_type"] = "SP"
        try:
            insert_peer_row(conn, peer_table_dict)
            conn.commit()
            added = added + 1
        except IntegrityError:
            pass
        found = found + 1
    return found, added


if __name__ == "__main__":
    capture_providers_main()
