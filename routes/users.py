from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.user import User, user_fields

users = Blueprint("users", __name__)

@users.route("", methods=["GET"])
@marshal_with(user_fields)
def get_users():
    users = User.query.all()

    return users