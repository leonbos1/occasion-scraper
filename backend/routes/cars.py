from flask import Blueprint, jsonify, request
from flask_restful import abort, marshal_with, marshal
from sqlalchemy import func, inspect, and_

from ..extensions import db
from ..middleware import remove_disallowed_properties

from ..models.car import Car, car_fields

from time import sleep

cars = Blueprint("cars", __name__)


@marshal_with(car_fields)
@cars.route("", methods=["GET"])
def get_cars():
    columns = [c_attr for c_attr in inspect(
        Car).attrs if c_attr.key != 'base_image']

    cars = Car.query.with_entities(*columns).all()

    print(f"{len(cars)} cars fetched from db")

    cars = [car._asdict() for car in cars]

    return cars


@cars.route("/filters", methods=["GET"])
def get_filters():
    filters = [
        "brand",
        "model",
        "min_first_registration",
        "max_first_registration",
        "min_mileage",
        "max_mileage",
        "min_price",
        "max_price"
    ]

    return filters


@cars.route("/<int:page_number>/<int:per_page>", methods=["POST"])
@marshal_with(car_fields)
def get_cars_page(page_number, per_page):
    request_json = request.json

    order_by = request_json.get("order_by", "created")
    order_direction = request_json.get("order_direction", "desc")
    filters = request_json.get("filters", {})

    query = Car.query

    for filter_name, filter_value in filters.items():
        print(filter_name, filter_value)
        if filter_value is not None:
            if type(filter_value) == str and len(filter_value) == 0:
                continue
            if filter_name.startswith("min_"):
                actual_filter = filter_name[4:]
                if hasattr(Car, actual_filter):
                    query = query.filter(
                        getattr(Car, actual_filter) >= filter_value)
            elif filter_name.startswith("max_"):
                actual_filter = filter_name[4:]
                if hasattr(Car, actual_filter):
                    query = query.filter(
                        getattr(Car, actual_filter) <= filter_value)
            elif hasattr(Car, filter_name):
                query = query.filter(getattr(Car, filter_name).like(f"%{filter_value}%"))

    query = query.order_by(getattr(Car, order_by).desc(
    ) if order_direction == "desc" else getattr(Car, order_by))
    page = query.paginate(page=page_number, per_page=per_page)

    cars = page.items

    for car in cars:
        car.created = car.created.split('.')[0]
        car.updated = car.updated.split('.')[0]

    print(f"{len(cars)} cars fetched from db")
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

@cars.route("/expensive/<int:count>", methods=["GET"])
@marshal_with(car_fields)
def get_expensive_cars(count):
    cars = Car.query.order_by(Car.price.desc()).limit(count).all()

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
    brands = db.session.query(Car.brand, func.count(
        Car.brand)).group_by(Car.brand).all()

    return {brand: count for brand, count in brands}


@cars.route("/models", methods=["GET"])
def get_models():
    models = db.session.query(Car.model, func.count(
        Car.model)).group_by(Car.model).all()

    return {model: count for model, count in models}

@cars.route("/count", methods=["GET"])
def get_car_count():
    car_count = Car.query.count()

    return jsonify(car_count)

@cars.route("/brands_and_models", methods=["GET"])
def get_brands_and_models():
    """
    Returns an object with brands as keys and a list of models as values
    """
    brands_and_models = db.session.query(Car.brand, Car.model).all()

    brands = {}

    for brand, model in brands_and_models:
        if brand not in brands:
            brands[brand] = []
        if model not in brands[brand]:
            brands[brand].append(model)

    return brands
