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

@blueprints.route("/<string:id>", methods=["GET"])
@marshal_with(blueprint_fields)
def get_blueprint(id):
    blueprint = BluePrint.query.get(id)

    if not blueprint:
        abort(404, message="Blueprint {} doesn't exist".format(id))

    return blueprint

@blueprints.route("", methods=["POST"])
@marshal_with(blueprint_fields)
def create_blueprint():
    data = request.get_json()

    #set all empty fields to None
    for key in data:
        if data[key] == "":
            data[key] = None

    blueprint = BluePrint(**data)

    db.session.add(blueprint)
    db.session.commit()

    return blueprint

@blueprints.route("/<string:id>", methods=["PUT"])
@marshal_with(blueprint_fields)
def update_blueprint(id):
    blueprint = BluePrint.query.get(id)

    if not blueprint:
        abort(404, message="Blueprint {} doesn't exist".format(id))

    data = request.get_json()
    blueprint.update(data)

    db.session.commit()

    return blueprint