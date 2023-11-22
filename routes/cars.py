from flask import Blueprint, jsonify, request
from flask_restful import abort
from flask_restful import marshal_with
from sqlalchemy import func

from ..extensions import db
from ..middleware import remove_disallowed_properties

from ..models.car import Car, car_fields

from time import sleep

cars = Blueprint("cars", __name__)

@cars.route("", methods=["GET"])
@marshal_with(car_fields)
def get_cars():
    cars = Car.query.all()

    for car in cars:
        car.base_image = ""

    print(f"{len(cars)} cars fetched from db")

    return cars

@cars.route("/<int:page_number>/<int:per_page>", methods=["POST"])
@marshal_with(car_fields)
def get_cars_page(page_number, per_page):
    request_json = request.json

    order_by = request_json.get("order_by", "created")
    order_direction = request_json.get("order_direction", "desc")

    query = Car.query.order_by(getattr(Car, order_by).desc() if order_direction == "desc" else getattr(Car, order_by))
    page = query.paginate(page=page_number, per_page=per_page)

    cars = page.items

    for car in cars:
        car.created = car.created.split('.')[0]
        car.updated = car.updated.split('.')[0]

    return cars

@cars.route("/max_page/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    max_page = Car.query.paginate(per_page=per_page).pages

    return jsonify(max_page)

@cars.route("/<string:id>", methods=["GET"])
@marshal_with(car_fields)
def get_car(id):
    car = Car.query.filter_by(id=id).first()

    return car

@cars.route("/recent/<int:count>", methods=["GET"])
@marshal_with(car_fields)
def get_recent_cars(count):
    cars = Car.query.order_by(Car.created.desc()).limit(count).all()

    return cars

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

@cars.route("/brands", methods=["GET"])
def get_brands():
    brands = db.session.query(Car.brand, func.count(Car.brand)).group_by(Car.brand).all()

    sleep(1)

    return {brand: count for brand, count in brands}