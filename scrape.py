from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
import os
import json
import time
from sqlalchemy.orm import Session
from utills.mail import send_email
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from extensions import Base, CREDENTIALS, url
from models.car import Car
from models.scrape_session import ScrapeSession


SYNC = True
MAX_DISTANCE_FROM_HOME = 50
MAX_PRICE = 3500
CITY = "appingedam"
FUEL_TYPE = "B"
MIN_MILEAGE = 100000
BODY_TYPE = 1

URL = f"https://www.autoscout24.nl/lst?atype=C&body={BODY_TYPE}&cy=NL&desc=0&fuel={FUEL_TYPE}&kmfrom={MIN_MILEAGE}&lat=53.3202659&lon=6.8575082&powertype=hp&priceto={MAX_PRICE}&search_id=4ujb49prb0&sort=standard&source=detailsearch&ustate=N%2CU&zip={CITY}&zipr={MAX_DISTANCE_FROM_HOME}"

with open("emails.json", "r") as f:
    EMAILS = json.load(f)["emails"]

engine = sqlalchemy.create_engine(url)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def main():
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    cars = []

    driver.get(URL)
    sleep(2)
    accept_cookies(driver)
    sleep(0.5)

    scrape_page(driver, cars)


def scrape_page(driver: webdriver, cars: list):
    main = driver.find_element_by_class_name("ListPage_main__L0gsf")
    scroll = 500
    scrape_session = ScrapeSession()
    save_session_to_db(scrape_session)

    for i in range(0, 1):
        sleep(1)
        articles = main.find_elements_by_tag_name("article")

        for article in articles:
            driver.execute_script(f"window.scrollBy(0, {scroll});")

            sleep(0.2)

            try:
                location_span = article.find_element_by_class_name(
                    "SellerInfo_address__txoNV")
                location_text = location_span.text.split("•")
                location = location_text[1]

            except Exception as e:
                all_elements = article.find_elements_by_tag_name("span")
                location = all_elements[-1].text

            try:
                img = article.find_element_by_class_name(
                    "NewGallery_img__bi92g")
                image = img.get_attribute("src")
                request = requests.get(image)
                image = request.content

            except NoSuchElementException:
                path = os.path.abspath("no-picture.png")
                with open(path, "rb") as f:
                    image = f.read()

            if article.get_attribute("data-mileage").isdigit():
                mileage = int(article.get_attribute("data-mileage"))

            else:
                mileage = 696969

            a_element = article.find_element_by_xpath(
                ".//a[contains(@class, 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l')]")
            href = a_element.get_attribute("href")
            car = Car(id=article.get_attribute("data-guid"), brand=article.get_attribute("data-make"), model=article.get_attribute("data-model"), price=article.get_attribute("data-price"),
                      mileage=mileage, first_registration=convert_to_year(article.get_attribute("data-first-registration")), vehicle_type=article.get_attribute("data-vehicle-type"),
                      location=location, image=image, condition=mileage, url=href, session_id=scrape_session.id)
            cars.append(car)

        driver.execute_script("window.scrollBy(0, -300);")

        try:
            next_page(driver)

        except:
            break

    new_cars = get_new_cars(cars)
    save_cars_to_db(new_cars)
    scrape_session.ended = time.time()
    scrape_session.new_cars = len(new_cars)
    save_session_to_db(scrape_session)

    if len(new_cars) > 0:
        send_email(new_cars, CREDENTIALS, EMAILS)

    driver.close()


def click_more_vehicles(driver: webdriver):
    more_vehicles_button = driver.find_element_by_xpath(
        "//button[contains(text(), 'More vehicles')]")
    more_vehicles_button.click()


def next_page(driver: webdriver):
    try:
        button = driver.find_element_by_xpath(
            "//button[contains(@class, 'FilteredListPagination') and contains(text(), 'Volgende')]")

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
    if first_registration.lower() == "new":
        return 2023

    else:
        return int(first_registration.split("-")[1])


def get_new_cars(cars: list):
    new_cars = []

    for car in cars:
        car_from_db = session.query(Car).filter(Car.id == car.id).first()

        if car_from_db == None:
            new_cars.append(car)

    return new_cars


def save_cars_to_db(cars: list):
    for car in cars:
        session.add(car)

    session.commit()


def save_session_to_db(scrape_session: ScrapeSession):
    if session.query(ScrapeSession).filter(ScrapeSession.id == scrape_session.id).first() == None:
        session.add(scrape_session)

    else:
        session.query(ScrapeSession).filter(ScrapeSession.id == scrape_session.id).update(
            {"ended": scrape_session.ended, "new_cars": scrape_session.new_cars})

    session.commit()


if __name__ == "__main__":
    main()
