from ..models.car import Car
from ..models.scrape_session import ScrapeSession
from ..extensions import db

def get_new_cars(cars: list):
    new_cars = []
    new_car_ids = []

    for car in cars:
        car_from_db = db.session.query(Car).filter(Car.id == car.id).first()

        if car_from_db == None and car.id not in new_car_ids:
            new_cars.append(car)
            new_car_ids.append(car.id)

    return new_cars


def save_cars_to_db(cars: list, logger):
    try:
        for car in cars:
            db.session.add(car)

        db.session.commit()
        logger.log_info(f"{len(cars)} new cars saved to db")

    except Exception as e:
        db.session.rollback()
        logger.log_error(str(e))


def save_session_to_db(scrape_session: ScrapeSession, logger):
    try:
        if db.session.query(ScrapeSession).filter(ScrapeSession.id == scrape_session.id).first() == None:
            db.session.add(scrape_session)

        else:
            db.session.query(ScrapeSession).filter(ScrapeSession.id == scrape_session.id).update(
                {"ended": scrape_session.ended, "new_cars": scrape_session.new_cars})
            
        db.session.commit()
        logger.log_info("Scrape session saved to db")
            
    except Exception as e:
        db.session.rollback()
        logger.log_error(str(e))