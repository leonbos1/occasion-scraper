from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.car import Car, resource_fields

cars = Blueprint("cars", __name__)



@cars.route("/", methods=["GET"])
@marshal_with(resource_fields)
def get_cars():
    cars = Car.query.all()

    return cars
