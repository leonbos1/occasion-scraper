from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.blueprint import BluePrint, blueprint_fields

blueprints = Blueprint("blueprints", __name__)

@blueprints.route("", methods=["GET"])
@marshal_with(blueprint_fields)
def get_blueprints():
    blueprints = BluePrint.query.all()

    return blueprints