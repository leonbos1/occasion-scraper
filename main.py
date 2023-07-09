from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
import sqlite3
import datetime
from requests import get
import os
import json
import smtplib

SYNC = True
MAX_DISTANCE_FROM_HOME = 50
MAX_PRICE = 3500
URL = f"https://www.autoscout24.nl/lst?atype=C&body=1&cy=NL&desc=0&fuel=B&kmfrom=100000&lat=53.3202659&lon=6.8575082&powertype=hp&priceto={MAX_PRICE}&search_id=4ujb49prb0&sort=standard&source=detailsearch&ustate=N%2CU&zip=9901%20appingedam&zipr={MAX_DISTANCE_FROM_HOME}"
EMAILS = ["bos.leon2001@gmail.com"]


def main():
    options = webdriver.FirefoxOptions()
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

    for i in range(0, 10):
        sleep(1)

        articles = main.find_elements_by_tag_name("article")

        for article in articles:
            try:
                location_span = article.find_element_by_class_name(
                    "SellerInfo_address__txoNV")
                location_text = location_span.text.split("•")
                location = location_text[1]
            except:
                location = "Niet bekend"

            driver.execute_script(f"window.scrollBy(0, {scroll});")

            sleep(0.2)
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

            car = Car(guid=article.get_attribute("data-guid"), brand=article.get_attribute("data-make"), model=article.get_attribute("data-model"), price=article.get_attribute("data-price"), mileage=mileage,
                      first_registration=convert_to_year(article.get_attribute("data-first-registration")), vehicle_type=article.get_attribute("data-vehicle-type"), location=location, image=image, condition=mileage)

            cars.append(car)

        driver.execute_script("window.scrollBy(0, -300);")

        try:
            next_page(driver)

        except:
            break

    new_cars = get_new_cars(cars)

    if SYNC:
        save_cars_to_db(new_cars)

    for car in new_cars:
        print(car)

    if len(new_cars) > 0:
        send_email(new_cars)


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
    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    c.execute("SELECT * FROM cars")

    db_cars = c.fetchall()

    new_cars = []

    guids = []

    for car in db_cars:
        guids.append(car[0])

    for car in cars:
        if car.guid not in guids:
            new_cars.append(car)

    return new_cars


def save_cars_to_db(cars: list):
    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    for car in cars:
        c.execute("INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (car.guid, car.brand, car.model,
                  car.price, car.mileage, car.first_registration, car.vehicle_type, car.location, car.image, car.condition))

    conn.commit()
    conn.close()


def send_email(cars: list):
    creds = json.load(open("credentials.json"))
    email = creds["email"]
    password = creds["password"]

    print(email)
    print(password)

    content = get_mail_content(cars)

    for email in EMAILS:
        with smtplib.SMTP(host="smtp.office365.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email, password)

            subject = "Nieuwe auto's op Autoscout24"

            msg = f"Subject: {subject}\n\n{content}"

            smtp.sendmail(email, email, msg)


def get_mail_content(cars: list):
    content = ""

    for car in cars:
        content += f"{car.brand} {car.model} {car.price} {car.mileage} {car.first_registration} {car.vehicle_type} {car.location} {car.condition}\n"

    return content


class Car:
    def __init__(self, guid: str, brand: str, model: str, price: str, mileage: int, first_registration: int, vehicle_type: str, location: str, image: bytes, condition: str):
        self.guid = guid
        self.brand = brand
        self.model = model
        self.price = price
        self.mileage = mileage
        self.first_registration = first_registration
        self.vehicle_type = vehicle_type
        self.location = location
        self.image = image
        self.condition = condition

    def __str__(self):
        return f"{self.brand} {self.model} {self.price} {self.mileage} {self.first_registration} {self.vehicle_type} {self.location} {self.condition}"


if __name__ == "__main__":
    cars = []
    send_email(cars)
