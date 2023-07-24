from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.car import Car, car_fields

cars = Blueprint("cars", __name__)

@cars.route("", methods=["GET"])
@marshal_with(car_fields)
def get_cars():
    cars = Car.query.all()

    return cars

@cars.route("/<int:id>", methods=["GET"])
@marshal_with(car_fields)
def get_car(id):
    car = Car.query.filter_by(id=id).first()

    return car

@cars.route("/", methods=["POST"])
@marshal_with(car_fields)
def create_car():
    brand = request.json["brand"]
    model = request.json["model"]
    price = request.json["price"]
    mileage = request.json["mileage"]
    first_registration = request.json["first_registration"]
    vehicle_type = request.json["vehicle_type"]
    location = request.json["location"]
    image = request.json["image"]
    condition = request.json["condition"]
    url = request.json["url"]
    session_id = request.json["session_id"]

    car = Car(brand, model, price, mileage, first_registration, vehicle_type, location, image, condition, url, session_id)
    db.session.add(car)
    db.session.commit()

    return car

@cars.route("/<int:id>", methods=["PUT"])
@marshal_with(car_fields)
def update_car(id):
    car = Car.query.filter_by(id=id).first()

    if not car:
        abort(404, message="Car not found")
    #make this less stupid 
    if "brand" in request.json:
        car.brand = request.json["brand"]
    if "model" in request.json:
        car.model = request.json["model"]
    if "price" in request.json:
        car.price = request.json["price"]
    if "mileage" in request.json:
        car.mileage = request.json["mileage"]
    if "first_registration" in request.json:
        car.first_registration = request.json["first_registration"]
    if "vehicle_type" in request.json:
        car.vehicle_type = request.json["vehicle_type"]
    if "location" in request.json:
        car.location = request.json["location"]
    if "image" in request.json:
        car.image = request.json["image"]
    if "condition" in request.json:
        car.condition = request.json["condition"]
    if "url" in request.json:
        car.url = request.json["url"]
    if "session_id" in request.json:
        car.session_id = request.json["session_id"]

    db.session.commit()

    return car