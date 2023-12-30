from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.blueprint import BluePrint, blueprint_fields

from ..routes.users import logged_in_required, admin_required

from ..middleware import remove_disallowed_properties

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

@blueprints.route("/<string:id>", methods=["DELETE"])
@marshal_with(blueprint_fields)
@logged_in_required
def delete_blueprint(current_user, id):
    blueprint = BluePrint.query.filter_by(id=id).first()

    if not blueprint:
        abort(404, message="Blueprint {} doesn't exist".format(id))

    if blueprint.owner_id != current_user.id:
        abort(403, message="You are not the owner of this blueprint")

    db.session.delete(blueprint)
    db.session.commit()

    return blueprint

@blueprints.route("/<int:page_number>/<int:per_page>", methods=["GET"])
@marshal_with(blueprint_fields)
def get_blueprints_page(page_number, per_page):
    page = BluePrint.query.paginate(page=page_number, per_page=per_page)

    blueprints = page.items

    return blueprints

@blueprints.route("/max_page/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    max_page = BluePrint.query.paginate(per_page=per_page).pages

    return jsonify(max_page)

@blueprints.route("", methods=["POST"])
@marshal_with(blueprint_fields)
@logged_in_required
def create_blueprint(current_user):
    data = request.get_json()

    for key in data:
        if data[key] == "":
            data[key] = None

    blueprint = BluePrint(**data)
    blueprint.owner_id = current_user.id

    db.session.add(blueprint)
    db.session.commit()

    return blueprint

@blueprints.route("/user/<int:size>", methods=["GET"])
@marshal_with(blueprint_fields)
@logged_in_required
def get_user_blueprints(current_user, size):
    blueprints = BluePrint.query.filter_by(owner_id=current_user.id).limit(size).all()

    return blueprints

@blueprints.route("/<string:id>", methods=["PUT"])
@marshal_with(blueprint_fields)
@remove_disallowed_properties()
def update_blueprint(id):
    blueprint = BluePrint.query.filter_by(id=id).first()

    if not blueprint:
        abort(404, message="blueprint not found")

    request_json = request._cached_json

    blueprint_properties = vars(blueprint)

    for prop in request_json:
        if prop in blueprint_properties:
            setattr(blueprint, prop, request_json[prop])

    db.session.commit()

    return blueprint