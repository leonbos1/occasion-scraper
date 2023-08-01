import requests
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

URL = "https://leonbos.nl:5000/start"

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def morning_scheduled_job():
    response = requests.get(URL)
    if response.status_code == 200:
        print("Morning scrape session started successfully.")
    else:
        print("Failed to start morning scrape session.")

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=19)
def evening_scheduled_job():
    response = requests.get(URL)
    if response.status_code == 200:
        print("Evening scrape session started successfully.")
    else:
        print("Failed to start evening scrape session.")

sched.start()