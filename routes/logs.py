from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.log import Log, log_fields

logs = Blueprint("logs", __name__)

@logs.route("", methods=["GET"])
@marshal_with(log_fields)
def get_logs():
    users = Log.query.all()

    return users