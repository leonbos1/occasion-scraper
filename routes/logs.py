from flask import Blueprint
from flask_restful import marshal_with
from ..models.log import Log, log_fields
from sqlalchemy import desc

logs = Blueprint("logs", __name__)

@logs.route("", methods=["GET"])
@marshal_with(log_fields)
def get_logs():
    logs = Log.query.order_by(desc(Log.created)).all()

    return logs