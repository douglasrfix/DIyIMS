from time import sleep

from diyims.beacon import beacon_main, satisfy_main
from diyims.peer_capture import (
    capture_providers_main,
    capture_bitswap_main,
    capture_swarm_main,
)
from diyims.ipfs_utils import wait_on_ipfs
from diyims.logger_utils import get_logger
from diyims.config_utils import get_scheduler_config_dict

# from diyims.capture_want_lists import process_peers
from multiprocessing import Process, set_start_method, freeze_support
from multiprocessing import Queue


def scheduler_main():
    if __name__ != "__main__":
        freeze_support()
        set_start_method("spawn")
    scheduler_config_dict = get_scheduler_config_dict()
    logger = get_logger(scheduler_config_dict["log_file"])
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    wait_seconds = int(scheduler_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Scheduler.")

    queue1 = Queue()
    queue2 = Queue()

    beacon_main_process = Process(target=beacon_main, args=(queue1, queue2))
    sleep(int(scheduler_config_dict["submit_delay"]))
    beacon_main_process.start()
    logger.debug("beacon_main started.")

    satisfy_main_process = Process(target=satisfy_main, args=(queue1, queue2))
    sleep(int(scheduler_config_dict["submit_delay"]))
    satisfy_main_process.start()
    logger.debug("satisfy_main started.")

    capture_providers_main_process = Process(target=capture_providers_main)
    sleep(int(scheduler_config_dict["submit_delay"]))
    capture_providers_main_process.start()
    logger.debug("capture_providers_main started.")

    capture_bitswap_main_process = Process(target=capture_bitswap_main)
    sleep(int(scheduler_config_dict["submit_delay"]))
    capture_bitswap_main_process.start()
    logger.debug("capture_bitswap_main started.")

    capture_swarm_main_process = Process(target=capture_swarm_main)
    sleep(int(scheduler_config_dict["submit_delay"]))
    capture_swarm_main_process.start()
    logger.debug("capture_swarm_main started.")

    beacon_main_process.join()
    satisfy_main_process.join()
    capture_providers_main_process.join()
    capture_bitswap_main_process.join()
    capture_swarm_main_process.join()
    logger.info("Normal shutdown of Scheduler.")

    return


if __name__ == "__main__":
    freeze_support()
    set_start_method("spawn")
    scheduler_main()
