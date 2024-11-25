"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.

Parameters:

year (int|str)              - 4-digit year
month (int|str)             - month (1-12)
day (int|str)               - day of month (1-31)
week (int|str)              - ISO week (1-53)
day_of_week (int|str)       - number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
hour (int|str)              - hour (0-23)
minute (int|str)            - minute (0-59)
second (int|str)            - second (0-59)
start_date (datetime|str)   - earliest possible date/time to trigger on (inclusive)
end_date (datetime|str)     - latest possible date/time to trigger on (inclusive)
timezone (datetime.tzinfo|str) - time zone to use for the date/time calculations (defaults to scheduler timezone)
jitter (int|None)           - delay the job execution by jitter seconds at most

Expression  Field   Description

*           any     Fire on every value
*/a         any     Fire every a values, starting from the minimum
a-b         any     Fire on any value within the a-b range (a must be smaller than b)
a-b/c       any     Fire every c values within the a-b range
xth y       day     Fire on the x -th occurrence of weekday y within the month
last x      day     Fire on the last occurrence of weekday x within the month
last        day     Fire on the last day within the month
x,y,z       any     Fire on any matching expression; can combine any number of any of the above expressions
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from time import sleep

from diyims.beacon import beacon_main
from diyims.satisfy import satisfy_main
from diyims.queue_server import queue_main
from diyims.ipfs_utils import wait_on_ipfs
from diyims.logger_utils import get_logger
from diyims.config_utils import get_scheduler_config_dict


def scheduler_main():
    scheduler_config_dict = get_scheduler_config_dict()
    logger = get_logger(scheduler_config_dict["log_file"])
    logger.info("Startup of Scheduler.")
    wait_on_ipfs(logger)
    logger.debug("Wait on ipfs completed.")
    executors = {
        "default": ProcessPoolExecutor(
            max_workers=int(scheduler_config_dict["worker_pool"])
        )
    }
    scheduler = BackgroundScheduler(executors=executors)
    scheduler.start()
    logger.debug("Scheduler start() completed.")
    scheduler.add_job(
        queue_main,
        "cron",
        hour="0-22",
        minute="*",
        second="*",
        max_instances=1,
        name="queue_main",
    )
    sleep(int(scheduler_config_dict["submit_delay"]))
    logger.debug("queue_main added.")
    scheduler.add_job(
        beacon_main,
        "cron",
        hour="0-22",
        minute="*",
        second="*",
        max_instances=1,
        name="beacon_main",
    )
    sleep(int(scheduler_config_dict["submit_delay"]))
    logger.debug("beacon_main added.")
    scheduler.add_job(
        satisfy_main,
        "cron",
        hour="0-22",
        minute="*",
        second="*",
        max_instances=1,
        name="satisfy_main",
    )
    sleep(int(scheduler_config_dict["submit_delay"]))
    logger.debug("satisfy_main added.")
    logger.debug("Scheduler shutdown().")
    scheduler.shutdown()
    logger.info("Scheduler shutdown() completed.")
    return


if __name__ == "__main__":
    scheduler_main()
