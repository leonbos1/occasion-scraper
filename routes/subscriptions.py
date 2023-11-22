from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.subscription import Subscription, subscription_fields, subscription_fields_with_blueprint
from ..models.blueprint import BluePrint

subscriptions = Blueprint("subscriptions", __name__)

@subscriptions.route("", methods=["GET"])
@marshal_with(subscription_fields)
def get_subscriptions():
    subscriptions = Subscription.query.all()

    return subscriptions

@subscriptions.route("/<int:page_number>/<int:per_page>", methods=["POST"])
@marshal_with(subscription_fields_with_blueprint)
def get_subscriptions_by_page(page_number, per_page):
    request_json = request.json

    order_by = request_json.get("order_by", "created")
    order_direction = request_json.get("order_direction", "desc")

    query = Subscription.query.join(BluePrint).order_by(
        getattr(Subscription, order_by).desc() if order_direction == "desc" else getattr(Subscription, order_by)
    )
    page = query.paginate(page=page_number, per_page=per_page)

    subscriptions = page.items

    for subscription in subscriptions:
        subscription.created = subscription.created.split('.')[0]
        subscription.updated = subscription.updated.split('.')[0]

    return subscriptions

@subscriptions.route("/<int:subscription_id>", methods=["GET"])
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
    db.session.add(subscription)
    db.session.commit()

    return subscription, 201

@subscriptions.route("/<int:subscription_id>", methods=["PUT"])
@marshal_with(subscription_fields)
def update_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        abort(404, message="Subscription {} doesn't exist".format(subscription_id))

    subscription.update(**request.json)
    db.session.commit()

    return subscription, 200

@subscriptions.route("/<int:subscription_id>", methods=["DELETE"])
@marshal_with(subscription_fields)
def delete_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        abort(404, message="Subscription {} doesn't exist".format(subscription_id))

    db.session.delete(subscription)
    db.session.commit()

    return subscription, 200

@subscriptions.route("/maxpage/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    max_page = Subscription.query.paginate(per_page=per_page).pages

    return jsonify(max_page)