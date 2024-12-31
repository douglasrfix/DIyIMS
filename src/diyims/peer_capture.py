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
from diyims.requests_utils import execute_request
from datetime import datetime, timezone
from sqlite3 import IntegrityError
from time import sleep
from multiprocessing.managers import BaseManager
from diyims.ipfs_utils import get_url_dict
from diyims.database_utils import (
    insert_peer_row,
    refresh_peer_table_dict,
    select_peer_table_entry_by_key,
    update_peer_table_peer_type_status,
    set_up_sql_operations,
)
from diyims.general_utils import get_network_name, get_shutdown_target
from diyims.logger_utils import get_logger
from diyims.config_utils import get_capture_peer_config_dict


def capture_peer_main(peer_type):
    capture_peer_config_dict = get_capture_peer_config_dict()
    logger = get_logger(capture_peer_config_dict["log_file"], peer_type)
    wait_seconds = int(capture_peer_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    if peer_type == "PP":
        logger.info("Startup of Provider Capture.")
    elif peer_type == "BP":
        logger.info("Startup of Bitswap Capture.")
    elif peer_type == "SP":
        logger.info("Startup of Swarm Capture.")
    interval_length = int(capture_peer_config_dict["capture_interval_delay"])
    target_DT = get_shutdown_target(capture_peer_config_dict)
    max_intervals = int(capture_peer_config_dict["max_intervals"])
    logger.info(
        f"Shutdown target {target_DT} or {max_intervals} intervals of {interval_length} seconds."
    )
    url_dict = get_url_dict()
    network_name = get_network_name()

    queue_server = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    if peer_type == "PP":
        queue_server.register("get_provider_queue")
        queue_server.connect()
        peer_queue = queue_server.get_provider_queue()

    elif peer_type == "BP":
        queue_server.register("get_bitswap_queue")
        queue_server.connect()
        peer_queue = queue_server.get_bitswap_queue()

    elif peer_type == "SP":
        queue_server.register("get_swarm_queue")
        queue_server.connect()
        peer_queue = queue_server.get_swarm_queue()

    capture_interval = 0
    total_found = 0
    total_added = 0
    total_promoted = 0
    current_DT = datetime.now()
    while target_DT > current_DT and capture_interval < max_intervals:
        conn, queries = set_up_sql_operations(capture_peer_config_dict)

        capture_interval += 1
        logger.debug(f"Start of Interval {capture_interval}")

        found, added, promoted = capture_peers(
            logger,
            conn,
            queries,
            capture_peer_config_dict,
            url_dict,
            peer_queue,
            peer_type,
            network_name,
        )

        total_found += found
        total_added += added
        total_promoted += promoted

        conn.close()
        logger.debug(f"Interval {capture_interval} complete.")
        sleep(int(capture_peer_config_dict["capture_interval_delay"]))
        current_DT = datetime.now()

    log_string = f"{total_found} {peer_type} found, {total_promoted} promoted and {total_added} added in {capture_interval} intervals)"
    logger.info(log_string)

    logger.info("Normal shutdown of Capture Process.")
    return


def capture_peers(
    logger,
    conn,
    queries,
    capture_peer_config_dict,
    url_dict,
    peer_queue,
    peer_type,
    network_name,
):
    param = {"arg": network_name}

    if peer_type == "PP":
        url_key = "find_providers"
        file = "none"
        config_dict = capture_peer_config_dict
        response = execute_request(
            logger,
            url_dict,
            url_key,
            config_dict,
            param,
            file,
        )

        found, added, promoted = decode_findprovs_structure(
            logger,
            conn,
            queries,
            capture_peer_config_dict,
            url_dict,
            response,
            peer_queue,
        )

    elif peer_type == "BP":
        url_key = "bitswap_stat"
        config_dict = capture_peer_config_dict
        file = "none"
        response = execute_request(
            logger,
            url_dict,
            url_key,
            config_dict,
            param,
            file,
        )

        found, added, promoted = decode_bitswap_stat_structure(
            logger,
            conn,
            queries,
            response,
            peer_queue,
        )

    elif peer_type == "SP":
        url_key = "swarm_peers"
        config_dict = capture_peer_config_dict
        file = "none"
        response = execute_request(
            logger,
            url_dict,
            url_key,
            config_dict,
            param,
            file,
        )

        found, added, promoted = decode_swarm_structure(
            logger,
            conn,
            queries,
            response,
            peer_queue,
        )

    return found, added, promoted


def decode_findprovs_structure(
    logger,
    conn,
    queries,
    capture_peer_config_dict,
    url_dict,
    r,
    peer_queue,
):
    found = 0
    added = 0
    promoted = 0
    peer_type = "PP"

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
                peer_table_dict["processing_status"] = "WLR"
                peer_table_dict["peer_ID"] = responses_dict["ID"]
                adr = False
                addrs_list = responses_dict["Addrs"]
                try:
                    peer_address = addrs_list[
                        0
                    ]  # the source for this is dht which may be present with out an address
                    adr = True

                except IndexError:
                    logger.debug("No Address 1")

                peer_table_dict["local_update_DTS"] = DTS
                peer_table_dict["peer_type"] = "PP"
                found += 1

                if adr is True:
                    try:
                        insert_peer_row(conn, queries, peer_table_dict)
                        conn.commit()
                        added += 1
                        if peer_table_dict["processing_status"] == "WLR":
                            param = {
                                "arg": peer_address + "/p2p/" + responses_dict["ID"]
                            }
                            url_key = "connect"
                            config_dict = capture_peer_config_dict
                            file = "none"
                            execute_request(
                                logger,
                                url_dict,
                                url_key,
                                config_dict,
                                param,
                                file,
                            )

                            url_key = "peering_add"
                            config_dict = capture_peer_config_dict
                            file = "none"
                            execute_request(
                                logger, url_dict, url_key, config_dict, param, file
                            )

                    except IntegrityError:  # Database
                        flag = False
                        peer_table_entry = select_peer_table_entry_by_key(
                            conn, queries, peer_table_dict
                        )
                        peer_type = peer_table_dict["peer_type"]

                        if peer_type == "BP":
                            peer_table_dict["peer_type"] = "PP"
                            peer_table_dict["processing_status"] = "WLR"
                            peer_table_dict["local_update_DTS"] = DTS
                            update_peer_table_peer_type_status(
                                conn, queries, peer_table_dict
                            )
                            promoted += 1
                            conn.commit()
                            flag = True

                        elif peer_table_entry["peer_type"] == "SP":
                            peer_table_dict["peer_type"] = "PP"
                            peer_table_dict["processing_status"] = "WLR"
                            peer_table_dict["local_update_DTS"] = DTS
                            update_peer_table_peer_type_status(
                                conn, queries, peer_table_dict
                            )
                            promoted += 1
                            conn.commit()
                            flag = True

                        if flag is True:
                            param = {
                                "arg": peer_address + "/p2p/" + responses_dict["ID"]
                            }
                            url_key = "connect"
                            config_dict = capture_peer_config_dict
                            file = "none"
                            execute_request(
                                logger,
                                url_dict,
                                url_key,
                                config_dict,
                                param,
                                file,
                            )

                            url_key = "peering_add"
                            config_dict = capture_peer_config_dict
                            file = "none"
                            execute_request(
                                logger,
                                url_dict,
                                url_key,
                                config_dict,
                                param,
                                file,
                            )

    if peer_type == "PP":  # wake up every interval for providers
        peer_queue.put_nowait("wake up")
        logger.debug("put wake up")

    if peer_type == "BP" and promoted != 0:
        peer_queue.put_nowait("promoted from bitswap wake up")
        logger.debug("put promoted from bitswap wake up")

    elif peer_type == "SP" and promoted != 0:
        peer_queue.put_nowait("promoted from swarm wake up")
        logger.debug("put promoted from swarm wake up")

    log_string = f"{found} providers found, {added} added and {promoted} promoted."
    logger.info(log_string)
    return found, added, promoted


def decode_bitswap_stat_structure(
    logger,
    conn,
    queries,
    r,
    peer_queue,
):
    found = 0
    added = 0
    promoted = 0
    json_dict = json.loads(r.text)
    peer_list = json_dict["Peers"]
    for peer in peer_list:
        peer_table_dict = refresh_peer_table_dict()
        DTS = str(datetime.now(timezone.utc))
        peer_table_dict["peer_ID"] = peer
        peer_table_dict["local_update_DTS"] = DTS
        peer_table_dict["peer_type"] = "BP"
        peer_table_dict["processing_status"] = (
            "WLR"  # BP and SP will continue processing until they exceed the
        )
        # zero want list threshold limit
        try:
            insert_peer_row(conn, queries, peer_table_dict)
            conn.commit()

            added += 1
        except IntegrityError:
            pass
        found += 1

    peer_queue.put_nowait("wake up")
    logger.debug("put wake up")
    log_string = f"{found} bitswap found and {added} added."
    logger.info(log_string)
    return found, added, promoted


def decode_swarm_structure(
    logger,
    conn,
    queries,
    r,
    peer_queue,
):
    level_zero_dict = json.loads(r.text)
    level_one_list = level_zero_dict["Peers"]
    found = 0
    added = 0
    promoted = 0
    for peer_dict in level_one_list:
        peer_table_dict = refresh_peer_table_dict()
        DTS = str(datetime.now(timezone.utc))
        peer_table_dict["peer_ID"] = peer_dict["Peer"]
        peer_table_dict["local_update_DTS"] = DTS
        peer_table_dict["peer_type"] = "SP"
        peer_table_dict["processing_status"] = "WLR"
        try:
            insert_peer_row(conn, queries, peer_table_dict)
            conn.commit()
            added += 1

        except IntegrityError:
            pass
        found += 1

    peer_queue.put_nowait("wake up")
    logger.debug("put wake up")
    log_string = f"{found} swarm found and {added} added."
    logger.info(log_string)
    return found, added, promoted


if __name__ == "__main__":
    capture_peer_main("PP")
