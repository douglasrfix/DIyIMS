import json
import psutil
from datetime import datetime
from time import sleep
from sqlite3 import IntegrityError
from multiprocessing import Pool, set_start_method, freeze_support
from multiprocessing.managers import BaseManager
from queue import Empty
from diyims.requests_utils import execute_request
from diyims.database_utils import (
    insert_want_list_row,
    select_want_list_entry_by_key,
    update_last_update_DTS,
    refresh_peer_table_dict,
    refresh_want_list_table_dict,
    set_up_sql_operations,
    update_peer_table_status_WLR,
    update_peer_table_status_WLP,
    update_peer_table_status_WLX,
    update_peer_table_status_WLZ,
)
from diyims.general_utils import get_DTS, get_shutdown_target
from diyims.ipfs_utils import get_url_dict
from diyims.logger_utils import get_logger, get_logger_task
from diyims.config_utils import get_want_list_config_dict


def capture_peer_want_lists(peer_type):  # each peer type runs in its own process
    freeze_support()
    try:
        set_start_method("spawn")
    except RuntimeError:
        pass
    p = psutil.Process()
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)  # NOTE: put in config
    want_list_config_dict = get_want_list_config_dict()
    logger = get_logger(
        want_list_config_dict["log_file"],
        peer_type,
    )
    wait_seconds = int(want_list_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Want List Capture.")
    target_DT = get_shutdown_target(want_list_config_dict)

    max_intervals = int(want_list_config_dict["max_intervals"])
    number_of_samples_per_interval = int(
        want_list_config_dict["number_of_samples_per_interval"]
    )
    seconds_per_sample = 60 // int(want_list_config_dict["samples_per_minute"])
    total_seconds = number_of_samples_per_interval * seconds_per_sample
    wait_for_new_peer = 60 * int(want_list_config_dict["wait_for_new_peer_minutes"])
    logger.info(
        f"Shutdown target {target_DT} or {max_intervals} intervals of {total_seconds} seconds."
    )
    interval_count = 0
    total_peers_processed = 0

    queue_server = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    if peer_type == "PP":
        queue_server.register("get_provider_queue")
        queue_server.connect()
        peer_queue = queue_server.get_provider_queue()
        pool_workers = int(want_list_config_dict["provider_pool_workers"])
        maxtasks = int(want_list_config_dict["provider_maxtasks"])
    elif peer_type == "BP":
        queue_server.register("get_bitswap_queue")
        queue_server.connect()
        peer_queue = queue_server.get_bitswap_queue()
        pool_workers = int(want_list_config_dict["bitswap_pool_workers"])
        maxtasks = int(want_list_config_dict["bitswap_maxtasks"])
    elif peer_type == "SP":
        queue_server.register("get_swarm_queue")
        queue_server.connect()
        peer_queue = queue_server.get_swarm_queue()
        pool_workers = int(want_list_config_dict["swarm_pool_workers"])
        maxtasks = int(want_list_config_dict["swarm_maxtasks"])

    with Pool(processes=pool_workers, maxtasksperchild=maxtasks) as pool:
        # used to throttle how many peers are processed concurrently
        current_DT = datetime.now()
        while target_DT > current_DT:
            # find any available peers that were previously captured before waiting for new ones
            peers_processed = capture_want_lists_for_peers(
                logger,
                want_list_config_dict,
                peer_type,
                pool,
            )
            total_peers_processed += peers_processed
            log_string = f"{peers_processed} {peer_type} peers submitted for Want List processing."
            logger.debug(log_string)
            interval_count += 1
            try:
                msg = peer_queue.get(
                    timeout=wait_for_new_peer
                )  # comes from peer capture process
                logger.debug(msg)
            except Empty:
                logger.debug("Queue empty")

            except AttributeError:
                sleep(60)
            interval_count += 1
            current_DT = datetime.now()

        log_string = f"{total_peers_processed} {peer_type} peers submitted for Want List  processing."
        logger.info(log_string)
        logger.info("Normal shutdown of Want List Capture.")
    return


def capture_want_lists_for_peers(
    logger,
    want_list_config_dict,
    peer_type,
    pool,
):
    peers_processed = 0
    DTS = get_DTS()
    connR, queries = set_up_sql_operations(want_list_config_dict)
    connU, queries = set_up_sql_operations(want_list_config_dict)
    # dual connections avoid locking conflict with the read

    found = True
    while found:
        row_for_peer = queries.select_peers_by_peer_type_status(
            connR, peer_type=peer_type
        )
        while row_for_peer:
            peer_table_dict = refresh_peer_table_dict()
            peer_table_dict["peer_ID"] = row_for_peer["peer_ID"]
            peer_table_dict["peer_type"] = row_for_peer["peer_type"]
            peer_table_dict["processing_status"] = (
                "WLP"  # suppress resubmission by WLR -> WLP
            )
            peer_table_dict["local_update_DTS"] = DTS

            update_peer_table_status_WLP(connU, queries, peer_table_dict)
            connU.commit()
            pool.apply_async(
                submitted_capture_peer_want_list_by_id,
                args=(
                    want_list_config_dict,
                    peer_table_dict,
                ),
            )

            logger.debug(f"peer {peers_processed} id {peer_table_dict['peer_ID']}.")
            peers_processed += 1
            row_for_peer = queries.select_peers_by_peer_type_status(
                connR, peer_type=peer_type
            )

        found = False

    connR.close()
    connU.close()

    return peers_processed


def submitted_capture_peer_want_list_by_id(
    want_list_config_dict,
    peer_table_dict,
):
    p = psutil.Process()
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)  # NOTE: put in config
    peer_type = peer_table_dict["peer_type"]
    peer_ID = peer_table_dict["peer_ID"]
    logger = get_logger_task(peer_type, peer_ID)
    logger.debug(f"Want list capture for {peer_ID} of type {peer_type} started.")

    conn, queries = set_up_sql_operations(want_list_config_dict)
    DTS = get_DTS()
    peer_table_dict["processing_status"] = "WLX"
    peer_table_dict["local_update_DTS"] = DTS
    # indicate processing is active for this peer WLP -> WLX
    update_peer_table_status_WLX(conn, queries, peer_table_dict)
    conn.commit()
    conn.close

    queue_server = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    if peer_type == "PP":
        queue_server.register("get_provider_queue")
        queue_server.connect()
        peer_queue = queue_server.get_provider_queue()
        max_zero_sample_count = int(want_list_config_dict["provider_zero_sample_count"])
        # peer_table_dict["processing_status"] = "WLR"

    elif peer_type == "BP":
        queue_server.register("get_bitswap_queue")
        queue_server.connect()
        peer_queue = queue_server.get_bitswap_queue()
        max_zero_sample_count = int(want_list_config_dict["bitswap_zero_sample_count"])
        # peer_table_dict["processing_status"] = "WLR"

    elif peer_type == "SP":
        queue_server.register("get_swarm_queue")
        queue_server.connect()
        peer_queue = queue_server.get_swarm_queue()
        max_zero_sample_count = int(want_list_config_dict["bitswap_zero_sample_count"])
        # peer_table_dict["processing_status"] = "WLR"

    # this is one sample interval for one peer
    number_of_samples_per_interval = int(
        want_list_config_dict["number_of_samples_per_interval"]
    )  # per_interval
    seconds_per_sample = 60 // int(want_list_config_dict["samples_per_minute"])
    wait_seconds = seconds_per_sample
    samples = 0
    zero_sample_count = 0
    found = 0
    added = 0
    updated = 0
    total_found = 0
    total_added = 0
    total_updated = 0
    NCW_count = 0

    while (
        samples < number_of_samples_per_interval
        # NOTE: will this condition allow the wlz to be processed twice?
        and zero_sample_count <= max_zero_sample_count
        # provider peers have the threshold set to 1440 to provide an infinite processing cycle
    ):
        sleep(wait_seconds)
        found, added, updated = capture_peer_want_list_by_id(
            logger, want_list_config_dict, peer_table_dict
        )
        total_found += found
        total_added += added
        total_updated += updated

        if found == 0:
            zero_sample_count += 1
        else:
            zero_sample_count -= 1

        if (
            zero_sample_count == max_zero_sample_count
        ):  # sampling permanently completed due to no want list available for peer
            conn, queries = set_up_sql_operations(want_list_config_dict)
            peer_table_dict["processing_status"] = "WLZ"
            peer_table_dict["local_update_DTS"] = DTS
            update_peer_table_status_WLZ(conn, queries, peer_table_dict)
            conn.commit()
            conn.close
            NCW_count += 1  # BUG: how does this get to 2?

        samples += 1

    if zero_sample_count < max_zero_sample_count:  # sampling interval completed
        conn, queries = set_up_sql_operations(
            want_list_config_dict
        )  # set from WLX to WLR so sampling will be continued
        peer_table_dict["processing_status"] = "WLR"
        peer_table_dict["local_update_DTS"] = DTS
        update_peer_table_status_WLR(conn, queries, peer_table_dict)
        conn.commit()
        conn.close

    log_string = f"In {samples} samples, {total_found} found, {total_added} added, {total_updated} updated and NCW {NCW_count} count for {peer_ID}"
    logger.debug(log_string)
    logger.debug(f"Want list capture for {peer_ID} of type {peer_type} completed.")
    peer_queue.put_nowait("wake up")
    return


def capture_peer_want_list_by_id(
    logger,
    want_list_config_dict,
    peer_table_dict,
):  # This is one sample for a peer
    url_dict = get_url_dict()

    found = 0
    added = 0
    updated = 0

    param = {"peer": peer_table_dict["peer_ID"]}
    response = execute_request(
        url_key="want_list",
        logger=logger,
        url_dict=url_dict,
        config_dict=want_list_config_dict,
        param=param,
    )

    level_zero_dict = json.loads(response.text)
    found, added, updated = decode_want_list_structure(
        want_list_config_dict, peer_table_dict, level_zero_dict
    )

    return found, added, updated


def decode_want_list_structure(want_list_config_dict, peer_table_dict, level_zero_dict):
    conn, queries = set_up_sql_operations(want_list_config_dict)
    found = 0
    added = 0
    updated = 0
    level_one_list = level_zero_dict["Keys"]
    if str(level_one_list) != "None":
        for level_two_dict in level_one_list:
            want_item = level_two_dict["/"]
            DTS = get_DTS()
            want_list_table_dict = refresh_want_list_table_dict()
            want_list_table_dict["peer_ID"] = peer_table_dict["peer_ID"]
            want_list_table_dict["object_CID"] = want_item
            want_list_table_dict["insert_DTS"] = DTS
            want_list_table_dict["source_peer_type"] = peer_table_dict["peer_type"]

            try:
                insert_want_list_row(conn, queries, want_list_table_dict)
                conn.commit()
                added += 1
            except IntegrityError:  # assumed to be dup key error
                want_list_entry = select_want_list_entry_by_key(
                    conn, queries, want_list_table_dict
                )
                want_list_table_dict["last_update_DTS"] = DTS
                insert_dt = datetime.fromisoformat(want_list_entry["insert_DTS"])
                update_dt = datetime.fromisoformat(
                    want_list_table_dict["last_update_DTS"]
                )
                delta = update_dt - insert_dt
                want_list_table_dict["insert_update_delta"] = int(delta.total_seconds())

                update_last_update_DTS(conn, queries, want_list_table_dict)
                conn.commit()
                updated += 1

            found += 1

    conn.close()
    return found, added, updated


if __name__ == "__main__":
    freeze_support()
    set_start_method("spawn")
    capture_peer_want_lists("PP")
