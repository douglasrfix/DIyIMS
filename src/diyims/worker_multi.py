from multiprocessing import Process, freeze_support, set_start_method

from diyims.beacon_utils import create_beacon_CID, satisfy_beacon
from diyims.worker_runner import run_worker
from dateutil.relativedelta import relativedelta
from datetime import datetime


def main(five_minute_intervals):
    freeze_support()
    set_start_method("spawn")
    target_date_time = relativedelta(months=+1)
    current_date_time = datetime.now()
    while target_date_time > current_date_time:
        beacon_CID, satisfy_CID = create_beacon_CID()

        for _ in range(4):  # "0000" 80
            process = Process(target=run_worker, args=(beacon_CID,))
            process.start()
            process.join(timeout=20)
            satisfy_beacon(satisfy_CID)
        for _ in range(4):  # "1" 160 240
            beacon_CID, satisfy_CID = create_beacon_CID()
            process = Process(target=run_worker, args=(beacon_CID,))
            process.start()
            process.join(timeout=40)
            satisfy_beacon(satisfy_CID)
        for _ in range(0):  # "0" 210
            beacon_CID, satisfy_CID = create_beacon_CID()
            process = Process(target=run_worker, args=(beacon_CID,))
            process.start()
            process.join(timeout=20)
            satisfy_beacon(satisfy_CID)
        for _ in range(0):  # "11" 220
            beacon_CID, satisfy_CID = create_beacon_CID()
            process = Process(target=run_worker, args=(beacon_CID,))
            process.start()
            process.join(timeout=40)
            satisfy_beacon(satisfy_CID)
        for _ in range(0):  # "0000" 300
            beacon_CID, satisfy_CID = create_beacon_CID()
            process = Process(target=run_worker, args=(beacon_CID,))
            process.start()
            process.join(timeout=20)
            satisfy_beacon(satisfy_CID)

    return
