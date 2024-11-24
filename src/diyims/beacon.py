from multiprocessing.managers import BaseManager
from diyims.beacon_utils import (
    create_beacon_CID,
    purge_want_items,
    flash_beacon,
    get_beacon_dict,
)
from dateutil.relativedelta import relativedelta
from datetime import datetime

from diyims.logger_utils import get_logger


def beacon_main():
    logger = get_logger("beacon.log")
    logger.info("Startup of Beacon.")
    # sleep(20)
    purge_want_items()  # NOTE: remove after testing
    manager = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    manager.register("get_queue1")
    manager.register("get_queue2")
    manager.connect()
    queue1 = manager.get_queue1()
    queue2 = manager.get_queue2()
    beacon_dict = get_beacon_dict()
    satisfy_dict = {}
    current_DT = datetime.now()
    current_date = current_DT.date()
    mid_night = relativedelta(hour=23, minute=59, second=59)
    before_midnight = relativedelta(hours=+int(beacon_dict["shutdown_offset_hours"]))
    current_DT = datetime.now()
    target_DT = current_date + mid_night - before_midnight

    logger.debug(f"Midnight {mid_night}")
    logger.debug(f"Before midnight {before_midnight}")
    logger.debug(f"Now {current_DT}")
    logger.info(f"Shutdown target {target_DT}")

    while target_DT > current_DT:
        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger)
            satisfy_dict["status"] = "run"
            satisfy_dict["wait_time"] = beacon_dict["short_period_seconds"]
            satisfy_dict["want_item_file"] = want_item_file
            queue1.put(satisfy_dict)
            message = queue2.get()
            logger.debug(message)

            flash_beacon(logger, beacon_CID)

        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger)
            satisfy_dict["status"] = "run"
            satisfy_dict["wait_time"] = beacon_dict["long_period_seconds"]
            satisfy_dict["want_item_file"] = want_item_file
            queue1.put(satisfy_dict)
            message = queue2.get()
            logger.debug(message)

            flash_beacon(logger, beacon_CID)

        current_DT = datetime.now()
    satisfy_dict["status"] = "shutdown"
    queue1.put(satisfy_dict)
    message = queue2.get()
    logger.info(f"Satisfy status {message}")
    logger.info("Normal shutdown of Beacon.")
    return


if __name__ == "__main__":
    beacon_main()
