from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db
from ..utills.user import generate_token, user_is_owner
from ..utills.responses import success_response, error_response, not_found_error, validation_error, auth_error, ErrorCodes

from ..models.user import User, user_fields
from ..models.subscription import Subscription

from functools import wraps

users = Blueprint("users", __name__)


def logged_in_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return auth_error("Authorization header required")

        user = User.query.filter_by(token=token).first()
        if not user:
            return auth_error("Invalid token")

        return func(user, *args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return auth_error("Authorization header required")

        user = User.query.filter_by(token=token).first()
        if not user:
            return auth_error("Invalid token")

        if user.role != "1":
            return error_response(ErrorCodes.AUTH_ERROR, "Admin role required", 403)

        return func(*args, **kwargs)

    return wrapper


@users.route("", methods=["GET"])
@admin_required
@logged_in_required
def get_users(current_user):
    """Get all users (admin only)"""
    try:
        users_list = User.query.all()
        result = []
        for user in users_list:
            user_dict = marshal(user, user_fields)
            user_dict['created'] = str(user.created).split('.')[0]
            user_dict['updated'] = str(user.updated).split('.')[0]
            result.append(user_dict)
        return success_response(result)
    except Exception as e:
        print(f"Error fetching users: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch users", 500)


@users.route("/<string:user_id>", methods=["PUT"])
@logged_in_required
def update_user(current_user, user_id):
    """Update user (owner or admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return validation_error("Request body is required")
        
        user = User.query.filter_by(id=user_id).first()

        if not user or not user_is_owner(current_user, user):
            return not_found_error("User not found")

        if data.get("email"):
            user.email = data.get("email")

        if data.get("password"):
            user.password = data.get("password")

        if user.role == "1" and data.get("role"):
            user.role = data.get("role")

        db.session.commit()
        
        user_dict = marshal(user, user_fields)
        user_dict['created'] = str(user.created).split('.')[0]
        user_dict['updated'] = str(user.updated).split('.')[0]

        return success_response(user_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to update user", 500)


@users.route("/<string:user_id>", methods=["DELETE"])
@logged_in_required
def delete_user(current_user, user_id):
    """Delete user (owner or admin only)"""
    try:
        user = User.query.filter_by(id=user_id).first()

        if not user or not user_is_owner(current_user, user):
            return not_found_error("User not found")

        db.session.delete(user)
        db.session.commit()
        
        user_dict = marshal(user, user_fields)
        user_dict['created'] = str(user.created).split('.')[0]
        user_dict['updated'] = str(user.updated).split('.')[0]

        return success_response(user_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to delete user", 500)


@users.route("register", methods=["POST"])
def create_user():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return validation_error("Request body is required")
        
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return validation_error("Email and password are required", {"fields": ["email", "password"]})

        user = User.query.filter_by(email=email).first()
        if user:
            return error_response(ErrorCodes.VALIDATION_ERROR, "Email already exists", 409)

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        user_dict = marshal(user, user_fields)
        user_dict['created'] = str(user.created).split('.')[0]
        user_dict['updated'] = str(user.updated).split('.')[0]

        return success_response(user_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to create user", 500)


@users.route("/login", methods=["POST"])
def login():
    """Login user and generate token"""
    try:
        data = request.get_json()
        
        if not data:
            return validation_error("Request body is required")
        
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return validation_error("Email and password are required", {"fields": ["email", "password"]})

        user = User.query.filter_by(email=email).first()
        if not user:
            return auth_error("Invalid email or password")

        # TODO: hash password
        if user.password != password:
            return auth_error("Invalid email or password")

        user.token = generate_token()
        db.session.commit()

        return success_response({"token": user.token, "role": user.role, "id": user.id})
    except Exception as e:
        print(f"Error during login: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Login failed", 500)


@users.route("/logout", methods=["POST"])
@logged_in_required
def logout(current_user):
    """Logout user and clear token"""
    try:
        current_user.token = None
        db.session.commit()

        return success_response({"message": "Logged out successfully"})
    except Exception as e:
        print(f"Error during logout: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Logout failed", 500)


@users.route("/profile", methods=["GET"])
@logged_in_required
def get_profile(current_user):
    """Get current user profile"""
    try:
        amount_of_blueprints_subscribed = Subscription.query.filter_by(
            user_id=current_user.id).count()

        result = {
            'email': current_user.email,
            'role': current_user.role,
            'created': str(current_user.created).split('.')[0],
            'updated': str(current_user.updated).split('.')[0],
            'amount_of_blueprints_subscribed': amount_of_blueprints_subscribed,
            'amount_of_blueprints_created': 0
        }

        return success_response(result)
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch profile", 500)


@users.route("/count", methods=["GET"])
def get_user_count():
    """Get total user count"""
    try:
        user_count = User.query.count()
        return success_response({"count": user_count})
    except Exception as e:
        print(f"Error counting users: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to count users", 500)