import os
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def morning_scheduled_job():
    os.system("python3 scrape.py")


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=19)
def evening_scheduled_job():
    os.system("python3 scrape.py")


sched.start()
