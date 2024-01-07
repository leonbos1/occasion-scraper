from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from sqlalchemy.orm import joinedload

from ..extensions import db

from ..models.subscription import Subscription, subscription_fields
from ..models.blueprint import BluePrint
from ..models.user import User

from ..routes.users import logged_in_required, admin_required

import datetime
import uuid

subscriptions = Blueprint("subscriptions", __name__)


@subscriptions.route("", methods=["GET"])
@marshal_with(subscription_fields)
def get_subscriptions():
    subscriptions = Subscription.query.all()

    return subscriptions


@subscriptions.route("/<int:page_number>/<int:per_page>", methods=["POST"])
@marshal_with(subscription_fields)
def get_subscriptions_by_page(page_number, per_page):
    request_json = request.json

    order_by = request_json.get("order_by", "created")
    order_direction = request_json.get("order_direction", "desc")

    query = Subscription.query.join(BluePrint).order_by(
        getattr(Subscription, order_by).desc(
        ) if order_direction == "desc" else getattr(Subscription, order_by)
    )
    page = query.paginate(page=page_number, per_page=per_page)

    subscriptions = page.items

    for subscription in subscriptions:
        subscription.created = subscription.created.split('.')[0]
        subscription.updated = subscription.updated.split('.')[0]

    return subscriptions


@subscriptions.route("/<string:subscription_id>", methods=["GET"])
@marshal_with(subscription_fields)
def get_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        abort(404, message="Subscription {} doesn't exist".format(subscription_id))

    return subscription


@subscriptions.route("", methods=["POST"])
@marshal_with(subscription_fields)
def create_subscription():
    subscription = Subscription(**request.json)

    existing_subscription = Subscription.query.filter_by(
        blueprint_id=subscription.blueprint_id, user_id=subscription.user_id).first()
    
    if existing_subscription:
        abort(409, message="Subscription already exists")

    #check if user exists
    user = User.query.get(subscription.user_id)
    if not user:
        abort(404, message="User {} doesn't exist".format(subscription.user_id))

    blueprint = BluePrint.query.get(subscription.blueprint_id)
    if not blueprint:
        abort(404, message="Blueprint {} doesn't exist".format(subscription.blueprint_id))

    subscription.id = str(uuid.uuid4())
    subscription.created = datetime.datetime.now()
    subscription.updated = datetime.datetime.now()

    db.session.add(subscription)
    db.session.commit()

    return subscription, 201


@subscriptions.route("/<string:subscription_id>", methods=["PUT"])
@marshal_with(subscription_fields)
@logged_in_required
def update_subscription(current_user, subscription_id):
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        abort(404, message="Subscription {} doesn't exist".format(subscription_id))

    if subscription.user_id != current_user.id:
        abort(403, message="You are not allowed to update this subscription")

    subscription.blueprint_id = request.json.get("blueprint_id", subscription.blueprint_id)
    subscription.user_id = request.json.get("user_id", subscription.user_id)
    subscription.updated = datetime.datetime.now()
    
    db.session.commit()

    return subscription, 200


@subscriptions.route("/<string:subscription_id>", methods=["DELETE"])
@marshal_with(subscription_fields)
@logged_in_required
def delete_subscription(current_user, subscription_id):
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        return f"Subscription {subscription_id} doesn't exist", 404
    
    if subscription.user_id != current_user.id:
        abort(403, message="You are not allowed to delete this subscription")

    db.session.delete(subscription)
    db.session.commit()

    return "Deleted!"


@subscriptions.route("/blueprint/<string:blueprint_id>", methods=["DELETE"])
@marshal_with(subscription_fields)
@logged_in_required
def delete_subscription_by_blueprint(current_user, blueprint_id):
    subscription = Subscription.query.filter_by(
        blueprint_id=blueprint_id, user_id=current_user.id).first()

    if not subscription:
        return f"Subscription with blueprint_id {blueprint_id} doesn't exist", 404

    db.session.delete(subscription)
    db.session.commit()

    return "Deleted!"

@subscriptions.route("/maxpage/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    max_page = Subscription.query.paginate(per_page=per_page).pages

    return jsonify(max_page)
