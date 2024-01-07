from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db
from ..utills.user import generate_token, user_is_owner

from ..models.user import User, user_fields
from ..models.subscription import Subscription

from functools import wraps

users = Blueprint("users", __name__)


def logged_in_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            abort(401, message="Authorization header required")

        user = User.query.filter_by(token=token).first()
        if not user:
            abort(401, message="Invalid token")

        return func(user, *args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            abort(401, message="Authorization header required")

        user = User.query.filter_by(token=token).first()
        if not user:
            abort(401, message="Invalid token")

        if user.role != "1":
            abort(403, message="Admin role required")

        return func(*args, **kwargs)

    return wrapper


@users.route("", methods=["GET"])
@marshal_with(user_fields)
@admin_required
@logged_in_required
def get_users(current_user):
    users = User.query.all()

    return users


@users.route("/<string:user_id>", methods=["PUT"])
@marshal_with(user_fields)
@logged_in_required
def update_user(current_user, user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()

    if not user or not user_is_owner(current_user, user):
        abort(404, message="User not found")

    if data.get("email"):
        user.email = data.get("email")

    if data.get("password"):
        user.password = data.get("password")

    if user.role == "1" and data.get("role"):
        user.role = data.get("role")

    db.session.commit()

    return user


@users.route("/<string:user_id>", methods=["DELETE"])
@marshal_with(user_fields)
@logged_in_required
def delete_user(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user or not user_is_owner(current_user, user):
        abort(404, message="User not found")

    db.session.delete(user)
    db.session.commit()

    return user


@users.route("register", methods=["POST"])
@marshal_with(user_fields)
def create_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        abort(409, message="Email already exists")

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return user, 201


@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        abort(401, message="Invalid email or password")

    # TODO: hash password
    if user.password != password:
        abort(401, message="Invalid email or password")

    user.token = generate_token()
    db.session.commit()

    return jsonify({"token": user.token, "role": user.role, "id": user.id})


@users.route("/logout", methods=["POST"])
@logged_in_required
def logout(current_user):
    current_user.token = None
    db.session.commit()

    return jsonify({"message": "Logged out successfully"})


@users.route("/profile", methods=["GET"])
@logged_in_required
def get_profile(current_user):

    amount_of_blueprints_subscribed = Subscription.query.filter_by(
        user_id=current_user.id).count()

    result = {
        'email': current_user.email,
        'role': current_user.role,
        'created': current_user.created,
        'updated': current_user.updated,
        'amount_of_blueprints_subscribed': amount_of_blueprints_subscribed,
        'amount_of_blueprints_created': 0
    }

    return jsonify(result)


@users.route("/count", methods=["GET"])
def get_user_count():
    user_count = User.query.count()

    return jsonify(user_count)