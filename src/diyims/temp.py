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


def main():
    wait_on_ipfs()
    executors = {"default": ProcessPoolExecutor(max_workers=3)}
    scheduler = BackgroundScheduler(executors=executors)
    scheduler.add_job(
        queue_main,
        "cron",
        hour="0-22",
        minute="*",
        second="*",
        max_instances=1,
        name="queue_main",
    )
    scheduler.add_job(
        beacon_main,
        "cron",
        hour="0-22",
        minute="*",
        second="*",
        max_instances=1,
        name="beacon_main",
    )
    scheduler.add_job(
        satisfy_main,
        "cron",
        hour="0-22",
        minute="*",
        second="*",
        max_instances=1,
        name="satisfy_main",
    )
    # scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.start()
    sleep(3)
    scheduler.shutdown()
    return


if __name__ == "__main__":
    main()
