import requests
import schedule
from time import sleep

URL = "http://leonbos.nl:5000/start"

def scheduled_job():
    response = requests.get(URL)
    if response.status_code == 200:
        print("GET request successful.")
    else:
        print("Failed to make GET request.")

schedule.every().day.at("07:00", "Europe/Amsterdam").do(scheduled_job)
schedule.every().day.at("19:00", "Europe/Amsterdam").do(scheduled_job)

while True:
    schedule.run_pending()
    sleep(10)