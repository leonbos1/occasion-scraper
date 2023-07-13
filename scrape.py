from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
import sqlite3
from requests import get
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import time

SYNC = True
MAX_DISTANCE_FROM_HOME = 50
MAX_PRICE = 3500
URL = f"https://www.autoscout24.nl/lst?atype=C&body=1&cy=NL&desc=0&fuel=B&kmfrom=100000&lat=53.3202659&lon=6.8575082&powertype=hp&priceto={MAX_PRICE}&search_id=4ujb49prb0&sort=standard&source=detailsearch&ustate=N%2CU&zip=9901%20appingedam&zipr={MAX_DISTANCE_FROM_HOME}"

with open("emails.json", "r") as f:
    EMAILS = json.load(f)["emails"]

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

            car = Car(guid=article.get_attribute("data-guid"), brand=article.get_attribute("data-make"), model=article.get_attribute("data-model"), price=article.get_attribute("data-price"), mileage=mileage,
                      first_registration=convert_to_year(article.get_attribute("data-first-registration")), vehicle_type=article.get_attribute("data-vehicle-type"), location=location, image=image, condition=mileage, url=href)

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
    from_email = creds["email"]
    password = creds["password"]

    content = get_mail_content(cars)

    for email in EMAILS:
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = email
        message["Subject"] = "Nieuwe auto's op autoscout24"

        message.attach(MIMEText(content, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, password)
            smtp.sendmail(from_email, email, message.as_string())


def get_mail_content(cars: list):
    content = ""

    # make a table
    content += "<table style='border: 1px solid black; border-collapse: collapse;'>"
    content += "<tr>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Merk</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Model</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Prijs</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Kilometerstand</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Bouwjaar</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Locatie</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>URL</th>"
    content += "</tr>"

    for car in cars:
        content += "<tr>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.brand}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.model}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>€{car.price}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.mileage}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.first_registration}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.location}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'><a href='{car.url}'>Link</a></td>"
        # image
        content += f"<td style='border: 1px solid black; padding: 5px;'><img src='data:image/png;base64,{base64.b64encode(car.image).decode('utf-8')}'></td>"

        content += "</tr>"

    return content


class Car:
    def __init__(self, guid: str, brand: str, model: str, price: str, mileage: int, first_registration: int, vehicle_type: str, location: str, image: bytes, condition: str, url: str):
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
        self.url = url

    def __str__(self):
        return f"{self.brand} {self.model} {self.price} {self.mileage} {self.first_registration} {self.vehicle_type} {self.location} {self.condition} {self.url}"


if __name__ == "__main__":
    main()
