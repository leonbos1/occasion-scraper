# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from time import sleep
# import requests
# import os
# import time
# from sqlalchemy.orm import Session
# from ..utills import mail
# import sqlalchemy
# from sqlalchemy.orm import sessionmaker
# from ..extensions import Base, url
# from ..models.car import Car
# from ..models.scrape_session import ScrapeSession
# from ..models.blueprint import BluePrint
# from ..models.subscription import Subscription
# from ..models.user import User
# from ..models.log import Log
# import datetime
# from uuid import uuid4

# BASE_URL = 'https://www.gaspedaal.nl'

# engine = sqlalchemy.create_engine(url)

# Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()


# def start():
#     global logger
#     options = webdriver.FirefoxOptions()
#     options.headless = False

#     driver = webdriver.Firefox(options=options)

#     cars = []

#     sleep(0.5)

#     try:
#         blueprints = session.query(BluePrint).all()

#         for blueprint in blueprints:
#             scrape_blueprint(driver, cars, blueprint)

#         driver.close()

#     except Exception as e:
#         print(e)
#         session.rollback()
#         driver.close()


# def scrape_blueprint(driver: webdriver, cars, blueprint: BluePrint):
#     global logger

#     url = BASE_URL

#     if blueprint.brand is not None:
#         url += "/" + blueprint.brand

#     elif blueprint.model is not None:
#         url += "/" + blueprint.model

#     else:
#         url += "/zoeken"

#     url += "?bmin=" + str(blueprint.min_first_registration) + \
#         "&bmax=" + str(blueprint.max_first_registration)

#     url += "&pmin=" + str(blueprint.min_price) + \
#         "&pmax=" + str(blueprint.max_price)

#     if blueprint.city is not None:
#         postal_code = blueprint.city.split(" ")[0]
#         url += "&pc=" + postal_code

#     if blueprint.max_distance_from_home is not None:
#         url += "&strl=" + str(blueprint.max_distance_from_home)

#     print(url)

#     driver.get(url)

#     driver.add_cookie({
#         "name": "consentUUID",
#         "value": "eb97b27f-7db1-42b2-96fc-69108f98a967_23",
#         "domain": ".gaspedaal.nl"
#     })

#     driver.add_cookie({
#         "name": "euconsent-v2",
#         "value": "CPxoFsAPxoFsAAGABBENDUCgAAAAAAAAABpYAAAAAAAAAAA",
#         "domain": ".gaspedaal.nl"
#     })

#     sleep(2)

#     accept_cookies(driver)

#     # class is flex w-full max-w-screen-xl flex-col self-center px-l
#     try:
#         main = driver.find_element_by_class_name(
#             "flex.w-full.max-w-screen-xl.flex-col.self-center.px-l")
        
#     except NoSuchElementException:
#         print("No cars found")
#         return
    
#     scroll = 500
#     scrape_session = ScrapeSession()
#     save_session_to_db(scrape_session)

#     logger = Logger(scrape_session.id)
#     logger.log_info("Scrape session started for gaspedaal.nl")

#     for i in range(0, 20):
#         sleep(1)

#         articles = main.find_elements_by_css_selector(
#             "div.min-w-\[250px\]:nth-child(1)")

#         for i, article in enumerate(articles, start=1):
#             driver.execute_script(f"window.scrollBy(0, {scroll});")
            
#             sleep(0.2)

#             location = article.find_element_by_css_selector(
#                 f"div.min-w-\[250px\]:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > p:nth-child(2)").text

#             try:
#                 img = article.find_element_by_css_selector(
#                     f"div.min-w-\[250px\]:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > img:nth-child(1)").get_attribute("src")
#                 req = requests.get(img)
#                 image = req.content

#             except NoSuchElementException:
#                 path = os.path.abspath("./occasion-scraper/no-image.png")
#                 with open(path, "rb") as f:
#                     image = f.read()

#             try:
#                 mileage = article.find_element_by_css_selector(
#                     f"div.min-w-\[250px\]:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(2) > p:nth-child(1) > span:nth-child(2)").text
#                 mileage = mileage.replace("km", "")
#                 mileage = mileage.replace(".", "")
#                 mileage = int(mileage)

#             except Exception:
#                 logger.log_error("Could not find mileage")
#                 mileage = 0

#             if blueprint.brand is not None:
#                 brand = blueprint.brand

#                 if blueprint.model is not None:
#                     model = blueprint.model

#             else:
#                 title = article.find_element_by_class_name(
#                     "font-bold text-xl ml-m flex-1 truncate pr-xs").text
#                 title = title.split(" ")
#                 brand = title[0]
#                 model = title[1]

#             first_registration = article.find_element_by_css_selector(
#                 f"div.min-w-\[250px\]:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(2) > p:nth-child(1) > span:nth-child(1)").text
#             price = article.find_element_by_css_selector(
#                 f"div.min-w-\[250px\]:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(1)").text
#             url = ''

#             id = uuid4()

#             car = Car(id=id, brand=brand, model=model, price=price,
#                       mileage=mileage, first_registration=first_registration, url=url, image=image, condition=mileage, vehicle_type='c', location=location, session_id=scrape_session.id)

#             cars.append(car)

#         driver.execute_script("window.scrollBy(0, -300);")

#         try:
#             next_page(driver)

#         except:
#             logger.log_info(f"No next page, {i} pages scraped")
#             break

#     new_cars = get_new_cars(cars)
#     logger.log_info(f"{len(new_cars)} new cars found")
#     save_cars_to_db(new_cars)
#     scrape_session.ended = time.time()
#     scrape_session.new_cars = len(new_cars)
#     save_session_to_db(scrape_session)

#     session = Session()

#     if len(new_cars) > 0:
#         emails = get_emails(blueprint)
#         mail.send_email(new_cars, emails, blueprint.name)
#         logger.log_info("Email sent")

#     logger.log_info("Scrape session ended")


# def accept_cookies(driver: webdriver):
#     try:
#         button = driver.find_element_by_xpath(
#             "//button[@title='Akkoord' and text()='Akkoord']")

#         button.click()

#         sleep(2)

#     except NoSuchElementException:
#         print("No cookies to accept")


# def get_emails(blueprint: BluePrint):
#     subscriptions = session.query(Subscription).filter_by(
#         blueprint_id=blueprint.id).all()

#     emails = []

#     for subscription in subscriptions:
#         emails.append(subscription.email)

#     return emails


# def click_more_vehicles(driver: webdriver):
#     more_vehicles_button = driver.find_element_by_xpath(
#         "//button[contains(text(), 'More vehicles')]")
#     more_vehicles_button.click()


# def next_page(driver: webdriver):
#     try:
#         button = driver.find_element_by_xpath(
#             "//button[contains(@aria-label, 'Ga naar volgende pagina')]")
#         button.click()

#     except NoSuchElementException:
#         print("No next page")


# def save_cars_to_db(cars):
#     for car in cars:
#         session.add(car)

#     session.commit()


# def save_session_to_db(scrape_session: ScrapeSession):
#     session.add(scrape_session)
#     session.commit()


# def get_new_cars(cars):
#     new_cars = []

#     for car in cars:
#         if session.query(Car).filter_by(url=car.url).first() is None:
#             new_cars.append(car)

#     return new_cars


# def get_new_cars(cars: list):
#     new_cars = []
#     new_car_ids = []

#     for car in cars:
#         car_from_db = session.query(Car).filter(Car.id == car.id).first()

#         if car_from_db == None and car.id not in new_car_ids:
#             new_cars.append(car)
#             new_car_ids.append(car.id)

#     return new_cars


# class Logger:
#     def __init__(self, session_id):
#         self.session_id = session_id

#     def log(self, message, level):
#         log = Log(
#             message=message,
#             level=level,
#             session_id=self.session_id
#         )

#         print(f"{datetime.datetime.now()} - {level} - {message}")

#         session.add(log)
#         session.commit()

#     def log_error(self, message):
#         self.log(message, 3)

#     def log_warning(self, message):
#         self.log(message, 2)

#     def log_info(self, message):
#         self.log(message, 1)


# if __name__ == "__main__":
#     start()
