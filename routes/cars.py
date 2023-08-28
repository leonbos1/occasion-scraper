from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db
from ..middleware import remove_disallowed_properties

from ..models.car import Car, car_fields

cars = Blueprint("cars", __name__)

#endpoint to get first 100 cars
@cars.route("/first100", methods=["GET"])
@marshal_with(car_fields)
def get_first100_cars():
    cars = Car.query.limit(100).all()

    print(f"{len(cars)} cars fetched from db")

    return cars


@cars.route("", methods=["GET"])
@marshal_with(car_fields)
def get_cars():
    cars = Car.query.all()

    for car in cars:
        car.base_image = ""

    print(f"{len(cars)} cars fetched from db")

    return cars


@cars.route("/<string:id>", methods=["GET"])
@marshal_with(car_fields)
def get_car(id):
    car = Car.query.filter_by(id=id).first()

    return car

@cars.route("/image/<string:id>", methods=["GET"])
def get_car_image(id):
    car = Car.query.filter_by(id=id).first()

    if car is None:
        abort(404, message="Car not found")

    return car.base_image

@cars.route("/", methods=["POST"])
@marshal_with(car_fields)
@remove_disallowed_properties()
def create_car():
    request_json = request._cached_json

    car = Car(**request_json)

    db.session.add(car)
    db.session.commit()

    return car


@cars.route("/<string:id>", methods=["PUT"])
@marshal_with(car_fields)
@remove_disallowed_properties()
def update_car(id):
    car = Car.query.filter_by(id=id).first()

    if not car:
        abort(404, message="Car not found")

    request_json = request._cached_json

    car_properties = vars(car)

    for prop in request_json:
        if prop in car_properties:
            setattr(car, prop, request_json[prop])

    db.session.commit()

    return car
