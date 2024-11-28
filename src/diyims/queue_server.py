from multiprocessing.managers import BaseManager
from multiprocessing import Queue
from time import sleep

from diyims.logger_utils import get_logger
from diyims.config_utils import get_queue_config_dict


def queue_main():
    queue_config_dict = get_queue_config_dict()
    logger = get_logger(queue_config_dict["log_file"])
    wait_seconds = int(queue_config_dict["wait_before_startup"])
    logger.debug(f"Waiting for {wait_seconds} seconds before startup.")
    sleep(wait_seconds)
    logger.info("Startup of Queue Server.")

    manager = BaseManager(address=("127.0.0.1", 50000), authkey=b"abc")
    queue1 = Queue()
    queue2 = Queue()
    manager.register("get_queue2", callable=lambda: queue2)
    manager.register("get_queue1", callable=lambda: queue1)

    server = manager.get_server()
    server.serve_forever()

    # while target_DT > current_DT:
    #     sleep(int(queue_config_dict["midnight_loop_delay"]))
    #     current_DT = datetime.now()

    # server.shutdown()
    # logger.info("Normal Shutdown of Queue Server.")

    return


if __name__ == "__main__":
    queue_main()
