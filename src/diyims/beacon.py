from multiprocessing.managers import BaseManager
from diyims.beacon_utils import (
    create_beacon_CID,
    purge_want_items,
    flash_beacon,
    get_beacon_dict,
)
from dateutil.relativedelta import relativedelta
from datetime import datetime
from time import sleep
from diyims.ipfs_utils import wait_on_ipfs

from diyims.logger_utils import get_logger


def beacon_main():
    sleep(20)
    wait_on_ipfs()
    logger = get_logger("beacon.log")
    logger.info("Startup of Beacon.")
    manager = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    manager.register("get_queue1")
    manager.register("get_queue2")
    manager.connect()
    queue1 = manager.get_queue1()
    queue2 = manager.get_queue2()

    purge_want_items()

    beacon_dict = get_beacon_dict()
    satisfy_dict = {}
    """
    if minutes_to_run != "Default":
        beacon_dict["minutes_to_run"] = minutes_to_run
    if long_period_seconds != "Default":
        beacon_dict["long_period_seconds"] = long_period_seconds
    if short_period_seconds != "Default":
        beacon_dict["short_period_seconds"] = short_period_seconds
    if number_of_periods != "Default":
        beacon_dict["number_of_periods"] = number_of_periods
    """
    current_DT = datetime.now()
    current_date = current_DT.date()
    delta = relativedelta(
        hour=23, minute=10, second=0
    )  # NOTE: get time to shut sown from config
    # delta = relativedelta(minutes=+5) # NOTE: get time to shut sown from config
    current_DT = datetime.now()
    target_DT = current_date + delta

    while target_DT > current_DT:
        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger)
            satisfy_dict["wait_time"] = beacon_dict["short_period_seconds"]
            satisfy_dict["want_item_file"] = want_item_file
            queue1.put(satisfy_dict)
            message = queue2.get()
            logger.debug(message)

            flash_beacon(logger, beacon_CID)

        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger)
            satisfy_dict["wait_time"] = beacon_dict["long_period_seconds"]
            satisfy_dict["want_item_file"] = want_item_file
            queue1.put(satisfy_dict)
            message = queue2.get()
            logger.debug(message)

            flash_beacon(logger, beacon_CID)

        current_DT = datetime.now()
    logger.info("Normal shutdown of Beacon.")
    return


if __name__ == "__main__":
    beacon_main()
