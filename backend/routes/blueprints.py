from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db
from ..utills.responses import success_response, error_response, not_found_error, validation_error, auth_error, ErrorCodes

from ..models.blueprint import BluePrint, blueprint_fields

from ..routes.users import logged_in_required, admin_required

from ..middleware import remove_disallowed_properties

blueprints = Blueprint("blueprints", __name__)


@blueprints.route("", methods=["GET"])
def get_blueprints():
    """Get all blueprints"""
    try:
        blueprints_list = BluePrint.query.all()
        result = []
        for bp in blueprints_list:
            bp_dict = marshal(bp, blueprint_fields)
            bp_dict['created'] = str(bp.created).split('.')[0]
            bp_dict['updated'] = str(bp.updated).split('.')[0]
            result.append(bp_dict)
        return success_response(result)
    except Exception as e:
        print(f"Error fetching blueprints: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch blueprints", 500)


@blueprints.route("/<string:id>", methods=["GET"])
def get_blueprint(id):
    """Get a single blueprint by ID"""
    blueprint = BluePrint.query.get(id)

    if not blueprint:
        return not_found_error(f"Blueprint {id} doesn't exist")
    
    bp_dict = marshal(blueprint, blueprint_fields)
    bp_dict['created'] = str(blueprint.created).split('.')[0]
    bp_dict['updated'] = str(blueprint.updated).split('.')[0]

    return success_response(bp_dict)


@blueprints.route("/<string:id>", methods=["DELETE"])
@logged_in_required
def delete_blueprint(current_user, id):
    """Delete a blueprint (owner only)"""
    try:
        blueprint = BluePrint.query.filter_by(id=id).first()

        if not blueprint:
            return not_found_error(f"Blueprint {id} doesn't exist")

        if blueprint.owner_id != current_user.id:
            return auth_error("You are not the owner of this blueprint")

        db.session.delete(blueprint)
        db.session.commit()
        
        bp_dict = marshal(blueprint, blueprint_fields)
        bp_dict['created'] = str(blueprint.created).split('.')[0]
        bp_dict['updated'] = str(blueprint.updated).split('.')[0]

        return success_response(bp_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting blueprint: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to delete blueprint", 500)


@blueprints.route("/<int:page_number>/<int:per_page>", methods=["GET"])
def get_blueprints_page(page_number, per_page):
    """Get paginated blueprints"""
    try:
        page = BluePrint.query.paginate(page=page_number, per_page=per_page)

        blueprints_list = []
        for bp in page.items:
            bp_dict = marshal(bp, blueprint_fields)
            bp_dict['created'] = str(bp.created).split('.')[0]
            bp_dict['updated'] = str(bp.updated).split('.')[0]
            blueprints_list.append(bp_dict)

        return success_response(blueprints_list, metadata={
            "page": page_number,
            "per_page": per_page,
            "total": page.total,
            "pages": page.pages
        })
    except Exception as e:
        print(f"Error fetching blueprint page: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch blueprints", 500)


@blueprints.route("/max_page/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    """Get maximum page number for pagination"""
    try:
        max_page = BluePrint.query.paginate(per_page=per_page).pages
        return success_response({"max_page": max_page})
    except Exception as e:
        print(f"Error getting max page: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to calculate pages", 500)


@blueprints.route("", methods=["POST"])
@logged_in_required
def create_blueprint(current_user):
    """Create a new blueprint"""
    try:
        data = request.get_json()
        
        if not data:
            return validation_error("Request body is required")

        for key in data:
            if data[key] == "":
                data[key] = None

        blueprint = BluePrint(**data)
        blueprint.owner_id = current_user.id

        db.session.add(blueprint)
        db.session.commit()
        
        bp_dict = marshal(blueprint, blueprint_fields)
        bp_dict['created'] = str(blueprint.created).split('.')[0]
        bp_dict['updated'] = str(blueprint.updated).split('.')[0]

        return success_response(bp_dict)
    except TypeError as e:
        return validation_error(f"Invalid blueprint data: {str(e)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating blueprint: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to create blueprint", 500)


@blueprints.route("/user/<int:size>", methods=["GET"])
@logged_in_required
def get_user_blueprints(current_user, size):
    """Get current user's blueprints"""
    try:
        blueprints_list = BluePrint.query.filter_by(
            owner_id=current_user.id).limit(size).all()
        
        result = []
        for bp in blueprints_list:
            bp_dict = marshal(bp, blueprint_fields)
            bp_dict['created'] = str(bp.created).split('.')[0]
            bp_dict['updated'] = str(bp.updated).split('.')[0]
            result.append(bp_dict)

        return success_response(result)
    except Exception as e:
        print(f"Error fetching user blueprints: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch blueprints", 500)


@blueprints.route("/<string:id>", methods=["PUT"])
@remove_disallowed_properties()
def update_blueprint(id):
    """Update an existing blueprint"""
    try:
        blueprint = BluePrint.query.filter_by(id=id).first()

        if not blueprint:
            return not_found_error("blueprint not found")

        request_json = request._cached_json
        
        if not request_json:
            return validation_error("Request body is required")

        blueprint_properties = vars(blueprint)

        for prop in request_json:
            if prop in blueprint_properties:
                setattr(blueprint, prop, request_json[prop])

        db.session.commit()
        
        bp_dict = marshal(blueprint, blueprint_fields)
        bp_dict['created'] = str(blueprint.created).split('.')[0]
        bp_dict['updated'] = str(blueprint.updated).split('.')[0]

        return success_response(bp_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error updating blueprint: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to update blueprint", 500)


@blueprints.route("/count", methods=["GET"])
def get_blueprint_count():
    """Get total blueprint count"""
    try:
        blueprints_count = BluePrint.query.count()
        return success_response({"count": blueprints_count})
    except Exception as e:
        print(f"Error counting blueprints: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to count blueprints", 500)
