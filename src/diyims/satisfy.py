from multiprocessing.managers import BaseManager
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
from diyims.logger_utils import get_logger
from diyims.beacon_utils import satisfy_beacon
from diyims.ipfs_utils import wait_on_ipfs


def satisfy_main():
    sleep(20)
    wait_on_ipfs()
    logger = get_logger("satisfy.log")
    logger.info("Startup of Satisfy.")
    # Create an instance of the Manager
    manager = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    # Create a queue within the context of the manager
    manager.register("get_queue2")
    manager.register("get_queue1")
    manager.connect()
    queue1 = manager.get_queue1()
    queue2 = manager.get_queue2()

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
        satisfy_dict = queue1.get()
        wait_time = int(satisfy_dict["wait_time"])
        want_item_file = satisfy_dict["want_item_file"]
        queue2.put("reply")
        sleep(wait_time)
        satisfy_beacon(logger, want_item_file)
        current_DT = datetime.now()

    logger.info("Normal shutdown of Satisfy.")
    return


# The following code will only run if the script is run directly
if __name__ == "__main__":
    satisfy_main()
