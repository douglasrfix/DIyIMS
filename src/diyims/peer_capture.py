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
from diyims.config_utils import get_peer_capture_config_dict


def peer_capture_main():
    peer_capture_config_dict = get_peer_capture_config_dict()
    logger = get_logger(peer_capture_config_dict["log_file"])
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    wait_seconds = int(peer_capture_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Peer Capture.")

    target_DT = get_shutdown_target(peer_capture_config_dict)
    current_DT = datetime.now()
    logger.info(f"Shutdown target {target_DT}")

    while target_DT > current_DT:
        sleep(int(peer_capture_config_dict["capture_interval_delay"]))
        capture_providers(logger, peer_capture_config_dict)
        current_DT = datetime.now()

    logger.info("Normal shutdown of Peer Capture.")
    return


def capture_providers(logger, peer_capture_config_dict):
    logger.info("Startup of Provider Capture.")

    url_dict = get_url_dict()
    path_dict = get_path_dict()
    network_name = get_network_name()
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(
        connect_path, timeout=int(peer_capture_config_dict["sql_timeout"])
    )
    key_arg = {"arg": network_name}
    i = 0
    not_found = True
    while i < int(peer_capture_config_dict["connect_retries"]) and not_found:
        try:
            with requests.post(
                url_dict["find_providers"], params=key_arg, stream=True
            ) as r:
                r.raise_for_status()
                not_found = False
                found, added = decode_findprovs_structure(conn, r)
        except ConnectionError:
            logger.exception()
            sleep(int(peer_capture_config_dict["connect_retry_delay"]))
            i += 1

    log_string = f"{found} providers found and {added} providers added to peer table"
    logger.info(log_string)
    logger.info("Provider Capture complete.")
    return


def decode_findprovs_structure(conn, r):
    found = 0
    added = 0
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            json_dict = json.loads(decoded_line)
            if json_dict["Type"] == 4:
                json_string = str(json_dict["Responses"])
                json_string_len = len(json_string)
                python_string = json_string[1 : json_string_len - 1]
                python_dict = json.loads(python_string.replace("'", '"'))
                # print(python_dict["ID"], json_dict["Type"])
                # provider_dict[python_dict["ID"]] = python_dict["ID"]

                peer_table_dict = refresh_peer_table_dict()
                DTS = str(datetime.now(timezone.utc))
                peer_table_dict["peer_ID"] = python_dict["ID"]
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

    return found, added


if __name__ == "__main__":
    peer_capture_main()
