from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import requests
import os
import json
import time
from sqlalchemy.orm import Session
from ..utills import mail, logger
from ..extensions import CREDENTIALS, session
from ..models.car import Car
from ..models.scrape_session import ScrapeSession
from ..models.blueprint import BluePrint
from ..models.subscription import Subscription
from ..utills.database import get_new_cars, save_cars_to_db, save_session_to_db
import datetime

BASE_URL = 'https://www.autoscout24.nl/lst'

with open("./occasion-scraper/emails.json", "r") as f:
    EMAILS = json.load(f)["emails"]

def start():
    global _logger
    options = webdriver.Chrome()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    cars = []

    sleep(0.5)

    try:
        blueprints = session.query(BluePrint).all()

        for blueprint in blueprints:
            scrape_blueprint(driver, cars, blueprint)

        driver.close()

    except Exception as e:
        print(e)
        print("Error occured, closing driver")
        session.rollback()
        driver.close()


def scrape_blueprint(driver: webdriver, cars: list, blueprint: BluePrint):
    global _logger

    url = BASE_URL

    if blueprint.brand != None:
        url += f"/{blueprint.brand}"

    if blueprint.model != None:
        url += f"/{blueprint.model}"

    url += "?cy=NL"

    url += f"&pricefrom={blueprint.min_price}"

    if blueprint.max_price > 0:
        url += f"&priceto={blueprint.max_price}"

    if blueprint.max_mileage > 0:
        url += f"&kmto={blueprint.max_mileage}"

    if blueprint.max_first_registration > 0:
        url += f"&fregto={blueprint.max_first_registration}"

    url += "&ustate=N%2CU"

    if blueprint.city != None and blueprint.max_distance_from_home > 0:
        url += f"&zip={blueprint.city}&zipr={blueprint.max_distance_from_home}"

    print(url)
    driver.get(url)

    sleep(2)
    accept_cookies(driver)

    main = driver.find_element_by_class_name("ListPage_main__L0gsf")
    scroll = 600
    scrape_session = ScrapeSession()
    save_session_to_db(scrape_session)

    _logger = logger.Logger(scrape_session.id)
    _logger.log_info(
        "Scrape session started for autoscout with blueprint: " + blueprint.name)

    for i in range(0, 20):
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(2)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article")))
            articles = main.find_elements_by_tag_name("article")
        except:
            _logger.log_error("No articles found")
            break

        for article in articles:
            id = article.get_attribute("id")

            try:
                driver.execute_script(f"window.scrollBy(0, {scroll});")

            except:
                _logger.log_error("Could not scroll")

            try:
                location_span = article.find_element_by_xpath(
                    ".//span[contains(@class, 'SellerInfo_address__txoNV')]")
                location_text = location_span.text.split("•")
                location = location_text[1]

            except Exception as e:
                all_elements = article.find_elements_by_tag_name("span")
                location = all_elements[-1].text

            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, "NewGallery_img__bi92g")))

                img = article.find_element_by_class_name(
                    "NewGallery_img__bi92g")
                image = img.get_attribute("src")
                request = requests.get(image)
                image = request.content

            except Exception as e:
                _logger.log_warning("Could not find image")
                path = os.path.abspath("./occasion-scraper/no-picture.png")
                with open(path, "rb") as f:
                    image = f.read()

            try:
                mileage = int(article.get_attribute("data-mileage"))

            except:
                _logger.log_warning("Could not find mileage")
                mileage = 0

            try:
                a_element = article.find_element_by_xpath(
                    ".//a[contains(@class, 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l')]")
                href = a_element.get_attribute("href")
            except Exception as e:
                _logger.log_error("Could not find href")

            try:
                sleep(1)
                article = driver.find_element_by_id(id)
                
                car = Car(id=article.get_attribute("data-guid"), brand=article.get_attribute("data-make"), model=article.get_attribute("data-model"), price=article.get_attribute("data-price"),
                          mileage=mileage, first_registration=convert_to_year(article.get_attribute("data-first-registration")), vehicle_type=article.get_attribute("data-vehicle-type"),
                          location=location, condition=mileage, url=href, session_id=scrape_session.id, image=image)
                cars.append(car)
            except Exception as e:
                _logger.log_error("Could not create car object: " + str(e))

        try:
            next_page(driver)

        except:
            _logger.log_info(f"No next page, {i} pages scraped")
            break

    new_cars = get_new_cars(cars)
    _logger.log_info(f"{len(new_cars)} new cars found")
    save_cars_to_db(new_cars, _logger)
    scrape_session.ended = datetime.datetime.now()
    scrape_session.new_cars = len(new_cars)
    save_session_to_db(scrape_session)

    if len(new_cars) > 0:
        emails = get_emails(blueprint)

        mail.send_email(new_cars, CREDENTIALS, emails, blueprint.name)
        _logger.log_info("Email sent")

    _logger.log_info("Scrape session ended")


def get_emails(blueprint: BluePrint):
    subscriptions = session.query(Subscription).filter_by(
        blueprint_id=blueprint.id).all()

    emails = []

    for subscription in subscriptions:
        emails.append(subscription.email)

    return emails


def click_more_vehicles(driver: webdriver):
    more_vehicles_button = driver.find_element_by_xpath(
        "//button[contains(text(), 'More vehicles')]")
    more_vehicles_button.click()


def next_page(driver: webdriver):
    try:
        button = driver.find_element_by_xpath(
            "//button[contains(@aria-label, 'Ga naar volgende pagina')]")
        button.click()

    except NoSuchElementException:
        print("No next page")


def accept_cookies(driver: webdriver):
    try:
        cookies_button = driver.find_element_by_xpath(
            "//button[contains(text(), 'Alles accepteren')]")
        cookies_button.click()

    except NoSuchElementException:
        print("No cookies button found")


def convert_to_year(first_registration: str):
    try:
        if first_registration.lower() == "new":
            return 2023

        else:
            return int(first_registration.split("-")[1])

    except:
        _logger.log_error(f"Could not convert {first_registration} to year")
        return 696969


if __name__ == "__main__":
    start()
