from multiprocessing import Process, freeze_support, set_start_method

from diyims.worker_runner import run_worker


def main():
    freeze_support()
    set_start_method("spawn")
    process = Process(target=run_worker)
    process.start()
    process.start()
    process.start()
    process.join()
