import requests
from apscheduler.schedulers.blocking import BlockingScheduler

URL = "http://example.com"

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=19)
def scheduled_job():
    response = requests.get(URL)
    if response.status_code == 200:
        print("GET request successful.")
    else:
        print("Failed to make GET request.")

sched.start()