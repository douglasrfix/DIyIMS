from multiprocessing import Process, freeze_support, set_start_method

from diyims.beacon_utils import create_beacon_CID, satisfy_beacon, get_beacon_dict
from beacon_runner import run_worker
from dateutil.relativedelta import relativedelta
from datetime import datetime


def main(minutes_to_run, long_period_seconds, short_period_seconds, number_of_periods):
    freeze_support()
    set_start_method("spawn")
    beacon_dict = get_beacon_dict()
    if minutes_to_run != "Default":
        beacon_dict["minutes_to_run"] = minutes_to_run

    current_DT = datetime.now()
    delta = relativedelta(minutes=+int(beacon_dict["minutes_to_run"]))
    target_DT = current_DT + delta
    current_DT = datetime.now()

    while target_DT > current_DT:
        for _ in range(int(beacon_dict["number_of_periods"])):
            beacon_CID, want_item_file = create_beacon_CID()
            process = Process(target=run_worker, args=(beacon_CID,))
            process.start()
            process.join(timeout=int(beacon_dict["short_period_seconds"]))
            satisfy_beacon(want_item_file)

        current_DT = datetime.now()
    return
