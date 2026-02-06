from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from sqlalchemy.orm import joinedload

from ..extensions import db
from ..utills.responses import success_response, error_response, not_found_error, validation_error, auth_error, ErrorCodes

from ..models.subscription import Subscription, subscription_fields
from ..models.blueprint import BluePrint
from ..models.user import User

from ..routes.users import logged_in_required, admin_required

import datetime
import uuid

subscriptions = Blueprint("subscriptions", __name__)


@subscriptions.route("", methods=["GET"])
def get_subscriptions():
    """Get all subscriptions"""
    try:
        subscriptions_list = Subscription.query.all()
        result = []
        for sub in subscriptions_list:
            sub_dict = marshal(sub, subscription_fields)
            sub_dict['created'] = str(sub.created).split('.')[0]
            sub_dict['updated'] = str(sub.updated).split('.')[0]
            result.append(sub_dict)
        return success_response(result)
    except Exception as e:
        print(f"Error fetching subscriptions: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch subscriptions", 500)


@subscriptions.route("/<int:page_number>/<int:per_page>", methods=["POST"])
def get_subscriptions_by_page(page_number, per_page):
    """Get paginated subscriptions with sorting"""
    try:
        request_json = request.json

        order_by = request_json.get("order_by", "created")
        order_direction = request_json.get("order_direction", "desc")
        
        if not hasattr(Subscription, order_by):
            return validation_error(f"Invalid order_by field: {order_by}")

        query = Subscription.query.join(BluePrint).order_by(
            getattr(Subscription, order_by).desc(
            ) if order_direction == "desc" else getattr(Subscription, order_by)
        )
        page = query.paginate(page=page_number, per_page=per_page)

        subscriptions_list = []
        for sub in page.items:
            sub_dict = marshal(sub, subscription_fields)
            sub_dict['created'] = str(sub.created).split('.')[0]
            sub_dict['updated'] = str(sub.updated).split('.')[0]
            subscriptions_list.append(sub_dict)

        return success_response(subscriptions_list, metadata={
            "page": page_number,
            "per_page": per_page,
            "total": page.total,
            "pages": page.pages
        })
    except Exception as e:
        print(f"Error fetching subscription page: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch subscriptions", 500)


@subscriptions.route("/<string:subscription_id>", methods=["GET"])
def get_subscription(subscription_id):
    """Get a single subscription by ID"""
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        return not_found_error(f"Subscription {subscription_id} doesn't exist")
    
    sub_dict = marshal(subscription, subscription_fields)
    sub_dict['created'] = str(subscription.created).split('.')[0]
    sub_dict['updated'] = str(subscription.updated).split('.')[0]

    return success_response(sub_dict)


@subscriptions.route("", methods=["POST"])
def create_subscription():
    """Create a new subscription"""
    try:
        data = request.json
        
        if not data:
            return validation_error("Request body is required")
        
        # Remove None values and exclude created/updated (handled by BaseModel)
        filtered_data = {k: v for k, v in data.items() if v is not None and k not in ['created', 'updated', 'id']}
        
        subscription = Subscription(**filtered_data)

        existing_subscription = Subscription.query.filter_by(
            blueprint_id=subscription.blueprint_id, user_id=subscription.user_id).first()
        
        if existing_subscription:
            return error_response(ErrorCodes.VALIDATION_ERROR, "Subscription already exists", 409)

        # Check if user exists
        user = User.query.get(subscription.user_id)
        if not user:
            return not_found_error(f"User {subscription.user_id} doesn't exist")

        blueprint = BluePrint.query.get(subscription.blueprint_id)
        if not blueprint:
            return not_found_error(f"Blueprint {subscription.blueprint_id} doesn't exist")

        # Note: BaseModel handles id, created, and updated automatically
        db.session.add(subscription)
        db.session.commit()
        
        sub_dict = marshal(subscription, subscription_fields)
        sub_dict['created'] = str(subscription.created).split('.')[0]
        sub_dict['updated'] = str(subscription.updated).split('.')[0]

        return success_response(sub_dict)
    except TypeError as e:
        return validation_error(f"Invalid subscription data: {str(e)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating subscription: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to create subscription", 500)


@subscriptions.route("/<string:subscription_id>", methods=["PUT"])
@logged_in_required
def update_subscription(current_user, subscription_id):
    """Update a subscription (owner only)"""
    try:
        subscription = Subscription.query.get(subscription_id)

        if not subscription:
            return not_found_error(f"Subscription {subscription_id} doesn't exist")

        if subscription.user_id != current_user.id:
            return auth_error("You are not allowed to update this subscription")
        
        data = request.json
        if not data:
            return validation_error("Request body is required")

        subscription.blueprint_id = data.get("blueprint_id", subscription.blueprint_id)
        subscription.user_id = data.get("user_id", subscription.user_id)
        # BaseModel updated timestamp handled automatically
        
        db.session.commit()
        
        sub_dict = marshal(subscription, subscription_fields)
        sub_dict['created'] = str(subscription.created).split('.')[0]
        sub_dict['updated'] = str(subscription.updated).split('.')[0]

        return success_response(sub_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error updating subscription: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to update subscription", 500)


@subscriptions.route("/<string:subscription_id>", methods=["DELETE"])
@logged_in_required
def delete_subscription(current_user, subscription_id):
    """Delete a subscription (owner only)"""
    try:
        subscription = Subscription.query.get(subscription_id)

        if not subscription:
            return not_found_error(f"Subscription {subscription_id} doesn't exist")
        
        if subscription.user_id != current_user.id:
            return auth_error("You are not allowed to delete this subscription")

        db.session.delete(subscription)
        db.session.commit()

        return success_response({"message": "Subscription deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting subscription: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to delete subscription", 500)


@subscriptions.route("/blueprint/<string:blueprint_id>", methods=["DELETE"])
@logged_in_required
def delete_subscription_by_blueprint(current_user, blueprint_id):
    """Delete a subscription by blueprint ID (owner only)"""
    try:
        subscription = Subscription.query.filter_by(
            blueprint_id=blueprint_id, user_id=current_user.id).first()

        if not subscription:
            return not_found_error(f"Subscription with blueprint_id {blueprint_id} doesn't exist")

        db.session.delete(subscription)
        db.session.commit()

        return success_response({"message": "Subscription deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting subscription: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to delete subscription", 500)

@subscriptions.route("/maxpage/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    """Get maximum page number for pagination"""
    try:
        max_page = Subscription.query.paginate(per_page=per_page).pages
        return success_response({"max_page": max_page})
    except Exception as e:
        print(f"Error getting max page: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to calculate pages", 500)
