from multiprocessing.managers import BaseManager
from time import sleep
from diyims.logger_utils import get_logger
from diyims.beacon_utils import satisfy_beacon


def satisfy_main():
    logger = get_logger("satisfy.log")
    logger.info("Startup of Satisfy.")
    # sleep(20)
    manager = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    manager.register("get_queue2")
    manager.register("get_queue1")
    manager.connect()
    queue1 = manager.get_queue1()
    queue2 = manager.get_queue2()

    satisfy_dict = queue1.get()

    while satisfy_dict["status"] == "run":
        wait_time = int(satisfy_dict["wait_time"])
        want_item_file = satisfy_dict["want_item_file"]
        queue2.put(satisfy_dict["status"])
        sleep(wait_time)
        satisfy_beacon(logger, want_item_file)
        satisfy_dict = queue1.get()

    queue2.put(satisfy_dict["status"])
    logger.info("Normal shutdown of Satisfy.")
    return