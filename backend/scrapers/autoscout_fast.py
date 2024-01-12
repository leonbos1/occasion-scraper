from time import sleep
import requests
import os
from sqlalchemy.orm import Session
from ..utills import mail, logger
from ..extensions import session
from ..models.car import Car
from ..models.scrape_session import ScrapeSession
from ..models.blueprint import BluePrint
from ..models.subscription import Subscription
from ..utills.database import get_new_cars, save_cars_to_db, save_session_to_db
import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://www.autoscout24.nl/'


def debug(text):
    with open("./log.txt", "a") as f:
        f.write(text + "\n")


def start():
    global _logger

    cars = []

    sleep(0.5)

    blueprints = session.query(BluePrint).all()

    for blueprint in blueprints:
        scrape_blueprint(cars, blueprint)


def scrape_blueprint(cars: list, blueprint: BluePrint):
    global _logger

    url = BASE_URL + "lst"

    scrape_session = ScrapeSession()

    _logger = logger.Logger(scrape_session.id)
    _logger.log_info(
        "Scrape session started for autoscout with blueprint: " + blueprint.name)

    save_session_to_db(scrape_session, _logger)

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

    new_cars_found = []

    for i in range(1, 20):
        cars = scrape_page(url + f"&page={i}", scrape_session)

        if len(cars) == 0:
            break

        new_cars = get_new_cars(cars)

        new_cars_found += new_cars

        save_cars_to_db(new_cars, _logger)
        scrape_session.ended = datetime.datetime.now()
        scrape_session.new_cars = len(new_cars)
        save_session_to_db(scrape_session, _logger)

    try:
        emails = get_emails(blueprint)
        for e in emails:
            _logger.log_info("Email: " + e)

    except Exception as e:
        _logger.log_error("Could not get emails" + str(e))
        emails = []

    try:
        mail.send_email(new_cars_found, emails, blueprint.name)
    except Exception as e:
        _logger.log_error("Could not send email" + str(e))

    _logger.log_info("Email sent")

    _logger.log_info("Scrape session ended")


def scrape_page(url: str, scrape_session: ScrapeSession) -> list:
    print(url)

    cars = []

    response = requests.get(url)

    if response.status_code != 200:
        _logger.log_error("Error while scraping autoscout")
        return

    try:
        articles = BeautifulSoup(
            response.text, "html.parser").find_all("article")
    except:
        _logger.log_error("Error while scraping autoscout")
        return

    if len(articles) == 0:
        return []

    for article in articles:
        try:
            car_id = article["data-guid"]
            if car_is_new(car_id) == False:
                continue

            location = get_location(article)
            condition = get_condition(article)
            url = get_href(article)

            image = get_image(url)

            car = Car(id=article["data-guid"], brand=article["data-make"], model=article["data-model"], price=article["data-price"],
                      mileage=article["data-mileage"], first_registration=convert_to_year(article["data-first-registration"]), vehicle_type=article["data-vehicle-type"],
                      location=location, condition=condition, url=url, session_id=scrape_session.id, image=image)

            cars.append(car)

        except Exception as e:
            print("Error while scraping car" + str(e))
            continue

    return cars


def get_emails(blueprint: BluePrint):
    subscriptions = session.query(Subscription).filter_by(
        blueprint_id=blueprint.id).all()

    emails = []

    for subscription in subscriptions:
        emails.append(subscription.user.email)

    return emails


def car_is_new(car_id: int):
    car = session.query(Car).filter_by(id=car_id).first()

    if car == None:
        return True

    return False


def get_href(article):
    try:
        a_element = article.find(
            "a", {"class": "ListItem_title__ndA4s ListItem_title_new_design__QIU2b Link_link__Ajn7I"})
        href = a_element["href"]

        return href

    except Exception as e:
        _logger.log_error("Could not find href")
        return ""


def get_condition(article):
    try:
        return int(article["data-mileage"])
    except:
        return 100420


def get_location(article):
    try:
        location_span = article.find(
            "span", {"class": "SellerInfo_address__txoNV"})
        location_text = location_span.text.split("•")

        return location_text[1]

    except Exception as e:
        all_elements = article.find_all("span")
        return all_elements[-1].text


def get_image(url):
    try:
        response = requests.get(BASE_URL + url)

        if response.status_code != 200:
            _logger.log_error("Could not find image")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        link_element = soup.find("link")
        image_url = link_element["href"]

        image_response = requests.get(image_url)

        if image_response.status_code != 200:
            _logger.log_error("Could not find image")
            return ""

        return image_response.content

    except Exception as e:
        _logger.log_error("Could not find image")
        return ""


def convert_to_year(first_registration: str):
    try:
        lowered_registration = first_registration.lower()

        if lowered_registration == "new":
            return 2023

        if lowered_registration == "used":
            return 2010

        if lowered_registration[2] == "-":
            return int(lowered_registration[3:])

        if lowered_registration[2] == "/":
            return int(lowered_registration[3:])

        else:
            return 2010

    except:
        return 2010


if __name__ == "__main__":
    start()
