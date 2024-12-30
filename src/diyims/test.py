import json
import requests

# import aiosql
from datetime import datetime, timezone
from sqlite3 import IntegrityError
from time import sleep
from rich import print
# from multiprocessing.managers import BaseManager
# from diyims.py_version_dep import get_sql_str

from diyims.ipfs_utils import get_url_dict

# from diyims.path_utils import get_path_dict
from diyims.database_utils import (
    #    insert_peer_row,
    refresh_peer_table_dict,
    select_peer_table_entry_by_key,
    #    update_peer_table_peer_type_status,
    set_up_sql_operations,
)
from diyims.general_utils import get_network_name, get_shutdown_target

# from diyims.logger_utils import get_logger
from diyims.config_utils import get_capture_peer_config_dict


def capture_peer_main(peer_type):
    capture_peer_config_dict = get_capture_peer_config_dict()
    # logger = get_logger(capture_peer_config_dict["log_file"], peer_type)
    # wait_on_ipfs(logger)
    # logger.debug("Wait on ipfs completed.")
    wait_seconds = int(capture_peer_config_dict["wait_before_startup"])
    # logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    # if peer_type == "PP":
    # logger.info("Startup of Provider Capture.")
    # elif peer_type == "BP":
    # logger.info("Startup of Bitswap Capture.")
    # elif peer_type == "SP":
    # logger.info("Startup of Swarm Capture.")
    # interval_length = int(capture_peer_config_dict["capture_interval_delay"])
    target_DT = get_shutdown_target(capture_peer_config_dict)
    max_intervals = int(capture_peer_config_dict["max_intervals"])
    # logger.info(
    #    f"Shutdown target {target_DT} or {max_intervals} intervals of {interval_length} seconds."
    # )
    url_dict = get_url_dict()
    network_name = get_network_name()

    capture_interval = 0
    total_found = 0
    total_added = 0
    total_promoted = 0
    current_DT = datetime.now()
    while target_DT > current_DT and capture_interval < max_intervals:
        conn, queries = set_up_sql_operations(capture_peer_config_dict)

        capture_interval += 1
        # logger.debug(f"Start of Interval {capture_interval}")

        found, added, promoted = capture_peers(
            # logger,
            conn,
            queries,
            capture_peer_config_dict,
            url_dict,
            #    peer_queue,
            peer_type,
            network_name,
        )

        total_found += found
        total_added += added
        total_promoted += promoted

        conn.close()
        # logger.debug(f"Interval {capture_interval} complete.")
        sleep(int(capture_peer_config_dict["capture_interval_delay"]))
        current_DT = datetime.now()

    # log_string = f"{total_found} {peer_type} found, {total_promoted} promoted and {total_added} added in {capture_interval} intervals)"
    # logger.info(log_string)

    # logger.info("Normal shutdown of Capture Process.")
    return


def capture_peers(
    # logger,
    conn,
    queries,
    capture_peer_config_dict,
    url_dict,
    #    peer_queue,
    peer_type,
    network_name,
):
    key_arg = {"arg": network_name}
    i = 0  # NOTE: fix this name
    not_found = True  # NOTE: fix this name
    while i < int(capture_peer_config_dict["connect_retries"]) and not_found:
        try:
            # logger.debug("start of requests")

            if peer_type == "PP":
                with requests.post(
                    url_dict["find_providers"], params=key_arg, stream=False
                ) as r:
                    r.raise_for_status()
                    # logger.debug("end of requests")
                    not_found = False

                found, added, promoted = decode_findprovs_structure(
                    # logger,
                    conn,
                    queries,
                    capture_peer_config_dict,
                    url_dict,
                    r,
                    # peer_queue,
                )

        except ConnectionError:
            # logger.exception()
            sleep(int(capture_peer_config_dict["connect_retry_delay"]))
            i += 1
    return found, added, promoted


def decode_findprovs_structure(
    # logger,
    conn,
    queries,
    capture_peer_config_dict,
    url_dict,
    r,
    # peer_queue,
):
    found = 0
    added = 0
    promoted = 0
    # peer_type = "PP"

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
                print(responses_dict["ID"])
                addrs_list = responses_dict["Addrs"]

                peer_table_dict = refresh_peer_table_dict()
                DTS = str(datetime.now(timezone.utc))
                peer_table_dict["peer_ID"] = responses_dict[
                    "ID"
                ]  # NOTE: capture a list of addresses and parse
                peer_table_dict["local_update_DTS"] = DTS
                peer_table_dict["processing_status"] = "WLP"
                peer_table_dict["peer_type"] = "PP"
                found += 1

                try:
                    # insert_peer_row(conn, queries, peer_table_dict) #NOTE: add address to peer table
                    conn.commit()
                    added += 1

                    addrs_list = responses_dict["Addrs"]
                    peer_address = addrs_list[0]
                    print(peer_address)
                    arg = {"arg": peer_address + "/p2p/" + responses_dict["ID"]}
                    print(arg)
                    skip = "12D3KooWDUvd28sw68KqoTxdqMWgLLPapavhLkFvbUY3WdzRqFGX"
                    i = 0
                    not_found = True
                    if skip == responses_dict["ID"]:
                        while (
                            i < int(capture_peer_config_dict["connect_retries"])
                            and not_found
                        ):
                            try:
                                # logger.debug("start of requests")
                                with requests.post(
                                    url_dict["connect"], params=arg, stream=False
                                ) as r:
                                    r.raise_for_status()
                                    # logger.debug("end of requests")
                                    not_found = False

                            except ConnectionError:
                                # logger.exception()
                                sleep(
                                    int(capture_peer_config_dict["connect_retry_delay"])
                                )

                                i += 1

                        i = 0
                        not_found = True
                        while (
                            i < int(capture_peer_config_dict["connect_retries"])
                            and not_found
                        ):
                            try:
                                # logger.debug("start of requests")
                                with requests.post(
                                    url_dict["peering_add"], params=arg, stream=False
                                ) as r:
                                    r.raise_for_status()
                                    # logger.debug("end of requests")
                                    not_found = False

                            except ConnectionError:
                                # logger.exception()
                                sleep(
                                    int(capture_peer_config_dict["connect_retry_delay"])
                                )
                                i += 1

                except IntegrityError:
                    peer_table_entry = select_peer_table_entry_by_key(
                        conn, queries, peer_table_dict
                    )
                    if peer_table_entry["peer_type"] == "BP":
                        peer_table_dict["peer_type"] = "PP"
                        peer_table_dict["processing_status"] = "WLP"
                        peer_table_dict["local_update_DTS"] = DTS
                        # update_peer_table_peer_type_status(
                        #    conn, queries, peer_table_dict
                        # )
                        promoted += 1
                        conn.commit()

                    elif peer_table_entry["peer_type"] == "SP":
                        peer_table_dict["peer_type"] = "PP"
                        peer_table_dict["processing_status"] = "WLP"
                        peer_table_dict["local_update_DTS"] = DTS
                        # update_peer_table_peer_type_status(
                        #    conn, queries, peer_table_dict
                        # )
                        promoted += 1
                        conn.commit()

    # log_string = f"{found} providers found, {added} added and {promoted} promoted."
    # logger.info(log_string)
    return found, added, promoted


def validate_ipv4(ip_address):
    import re

    ipv4_pattern = r"^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    pattern = ipv4_pattern
    if re.match(pattern, ip_address):
        return True
    return False


# Example usage:
ip_address = "192.168.1.100"
if validate_ipv4(ip_address):
    print(f"{ip_address} is a valid IPv4 address")
else:
    print(f"{ip_address} is not a valid IPv4 address")


if __name__ == "__main__":
    capture_peer_main("PP")
