# worker_runner.py
from diyims.beacon import do_work
from diyims.logger_utils import get_logger


def run_beacon(beacon_CID):
    logger = get_logger()
    do_work(logger, beacon_CID)

    return

    # if __name__ == '__main__':
    # not needed, as this script will be imported and executed by multiprocessing
    # pass
