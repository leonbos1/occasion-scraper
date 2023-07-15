from fastapi import FastAPI
from extensions import CREDENTIALS, url, Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.car import Car
import datetime

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
    session = get_session()

    start_timestamp = datetime.datetime.strptime(date, "%d-%m-%Y").timestamp()
    end_timestamp = start_timestamp + 86400

    cars = session.query(Car).filter(
        Car.created >= start_timestamp, Car.created <= end_timestamp).all()
    
    for car in cars:
        car.image = None

    session.close()

    return cars