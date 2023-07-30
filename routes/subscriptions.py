from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.subscription import Subscription, subscription_fields

subscriptions = Blueprint("subscriptions", __name__)

@subscriptions.route("", methods=["GET"])
@marshal_with(subscription_fields)
def get_users():
    users = Subscription.query.all()

    return users