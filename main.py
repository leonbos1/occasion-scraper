import os
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21)

def scheduled_job():
    os.system("python3 scrape.py")

sched.start()
