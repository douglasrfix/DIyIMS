from multiprocessing.managers import BaseManager
from multiprocessing import Queue
from dateutil.relativedelta import relativedelta
from datetime import datetime
from time import sleep

from diyims.logger_utils import get_logger


def queue_main():
    logger = get_logger("queue.log")
    logger.info("Startup of Queue Server.")
    manager = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    queue1 = Queue()
    queue2 = Queue()

    manager.register("get_queue2", callable=lambda: queue2)
    manager.register("get_queue1", callable=lambda: queue1)

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
    server = manager.get_server()
    server.serve_forever()

    while target_DT > current_DT:
        sleep(60)
        current_DT = datetime.now()

    server.shutdown()
    logger.info("Normal Shutdown of Queue Server.")
    return


if __name__ == "__main__":
    queue_main()
