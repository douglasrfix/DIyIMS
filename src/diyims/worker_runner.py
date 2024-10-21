# worker_runner.py
from diyims.worker import do_work


def run_worker():
    return do_work()

    # if __name__ == '__main__':
    # not needed, as this script will be imported and executed by multiprocessing
    # pass
