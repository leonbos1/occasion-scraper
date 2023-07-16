from fastapi import FastAPI
from extensions import CREDENTIALS, url, Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.car import Car
import datetime
import uvicorn

app = FastAPI()

engine = sqlalchemy.create_engine(url)
Base.metadata.create_all(bind=engine)


def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


@app.get("/cars")
def get_cars():
    session = get_session()

    cars = session.query(Car).all()

    for car in cars:
        car.image = None

    session.close()

    return cars


@app.get("/cars/{car_id}")
def get_car(car_id: str):
    session = get_session()

    car = session.query(Car).filter(Car.id == car_id).first()

    car.image = None

    session.close()

    return car


@app.get("/cars/session/{session_id}")
def get_cars_by_session(session_id: str):
    session = get_session()

    cars = session.query(Car).filter(Car.session_id == session_id).all()

    for car in cars:
        car.image = None

    session.close()

    return cars


@app.get("/cars/brand/{brand}")
def get_cars_by_brand(brand: str):
    session = get_session()

    cars = session.query(Car).filter(Car.brand == brand).all()

    for car in cars:
        car.image = None

    session.close()

    return cars


@app.get("/cars/brand/{brand}/model/{model}")
def get_cars_by_brand_and_model(brand: str, model: str):
    session = get_session()

    cars = session.query(Car).filter(
        Car.brand == brand, Car.model == model).all()

    for car in cars:
        car.image = None

    session.close()

    return cars


@app.get("/cars/session/{session_id}/amount")
def get_amount_of_cars_by_session(session_id: str):
    session = get_session()

    amount = session.query(Car).filter(Car.session_id == session_id).count()

    session.close()

    return amount

@app.get("/cars/date/{date}")
def get_cars_by_date(date: str):
    if date == "today":
        date = datetime.datetime.now().strftime("%d-%m-%Y")

    session = get_session()

    start_timestamp = datetime.datetime.strptime(date, "%d-%m-%Y").timestamp()
    end_timestamp = start_timestamp + 86400

    cars = session.query(Car).filter(
        Car.created >= start_timestamp, Car.created <= end_timestamp).all()
    
    for car in cars:
        car.image = None

    session.close()

    return cars

@app.get("/cars/date/today/amount")
def get_amount_of_cars_today():
    session = get_session()

    start_timestamp = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0).timestamp()
    end_timestamp = start_timestamp + 86400

    amount = session.query(Car).filter(
        Car.created >= start_timestamp, Car.created <= end_timestamp).count()

    session.close()

    return amount

#get latest car scraped
@app.get("/car/latest")
def get_latest_car():
    session = get_session()

    car = session.query(Car).order_by(Car.created.desc()).first()

    car.image = None

    session.close()

    return car