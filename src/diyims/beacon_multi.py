from multiprocessing import Process, freeze_support, set_start_method

from diyims.beacon_utils import (
    create_beacon_CID,
    purge_want_items,
    satisfy_beacon,
    get_beacon_dict,
)
from diyims.beacon_runner import run_beacon
from dateutil.relativedelta import relativedelta
from datetime import datetime
from time import sleep

from diyims.logger_utils import get_logger


def beacon_main(
    minutes_to_run, long_period_seconds, short_period_seconds, number_of_periods
):
    freeze_support()
    set_start_method("spawn")

    logger = get_logger()
    purge_want_items()
    sleep(120)
    logger.info("Startup of Beacon.")
    beacon_dict = get_beacon_dict()
    if minutes_to_run != "Default":
        beacon_dict["minutes_to_run"] = minutes_to_run
    if long_period_seconds != "Default":
        beacon_dict["long_period_seconds"] = long_period_seconds
    if short_period_seconds != "Default":
        beacon_dict["short_period_seconds"] = short_period_seconds
    if number_of_periods != "Default":
        beacon_dict["number_of_periods"] = number_of_periods

    current_DT = datetime.now()
    current_date = current_DT.date()
    delta = relativedelta(hour=23, minute=10, second=0)
    current_DT = datetime.now()
    target_DT = current_date + delta

    while target_DT > current_DT:
        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger)
            process = Process(target=run_beacon, args=(beacon_CID,))
            process.start()
            process.join(timeout=int(beacon_dict["short_period_seconds"]))
            satisfy_beacon(logger, want_item_file)

        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID(logger)
            process = Process(target=run_beacon, args=(beacon_CID,))
            process.start()
            process.join(timeout=int(beacon_dict["long_period_seconds"]))
            satisfy_beacon(logger, want_item_file)

        current_DT = datetime.now()
    logger.info("Normal shutdown of Beacon.")
    return
