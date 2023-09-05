from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
import os
import json
import time
from sqlalchemy.orm import Session
from ..utills import mail
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from ..extensions import Base, CREDENTIALS, url
from ..models.car import Car
from ..models.scrape_session import ScrapeSession
from ..models.blueprint import BluePrint
from ..models.subscription import Subscription
from ..models.user import User
from ..models.log import Log
import datetime

BASE_URL = 'https://www.gaspedaal.nl'

with open("./occasion-scraper/emails.json", "r") as f:
    EMAILS = json.load(f)["emails"]

engine = sqlalchemy.create_engine(url)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def start():
    global logger
    options = webdriver.FirefoxOptions()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    cars = []

    sleep(0.5)

    try:
        blueprints = session.query(BluePrint).all()

        for blueprint in blueprints:
            scrape_blueprint(driver, cars, blueprint)

        driver.close()

    except Exception as e:
        print(e)
        session.rollback()
        driver.close()


def scrape_blueprint(driver: webdriver, cars, blueprint: BluePrint):
    global logger

    url = BASE_URL

    if blueprint.brand is not None:
        url += "/" + blueprint.brand

    if blueprint.model is not None:
        url += "/" + blueprint.model

    url += "?bmin=" + str(blueprint.min_first_registration) + \
        "&bmax=" + str(blueprint.max_first_registration)

    url += "&pmin=" + str(blueprint.min_price) + \
        "&pmax=" + str(blueprint.max_price)

    if blueprint.city is not None:
        url += "&pc=" + blueprint.city

    if blueprint.max_distance_from_home is not None:
        url += "&strl=" + str(blueprint.max_distance_from_home)