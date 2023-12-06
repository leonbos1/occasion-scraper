from flask import Blueprint
from flask_restful import marshal_with
from ..models.log import Log, log_fields
from sqlalchemy import desc
from datetime import datetime, timedelta
from sqlalchemy import cast, Date

logs = Blueprint("logs", __name__)


@logs.route("", methods=["GET"])
@marshal_with(log_fields)
def get_logs():
    logs = Log.query.order_by(desc(Log.created)).all()

    return logs


@logs.route("/dashboard", methods=["GET"])
@marshal_with(log_fields)
def get_dashboard_logs():
    format = "%Y-%m-%d %H:%M:%S.%f"  # The format of your datetime string

    now = datetime.now()
    yesterday = now - timedelta(hours=24)
    last_week = now - timedelta(days=7)

    errors_24h = Log.query.filter(cast(Log.created, Date) >= datetime.strptime(
        yesterday.strftime(format), format)).filter(Log.level == 3).count()
    warnings_24h = Log.query.filter(cast(Log.created, Date) >= datetime.strptime(
        yesterday.strftime(format), format)).filter(Log.level == 2).count()
    errors_7d = Log.query.filter(cast(Log.created, Date) >= datetime.strptime(
        last_week.strftime(format), format)).filter(Log.level == 3).count()
    warnings_7d = Log.query.filter(cast(Log.created, Date) >= datetime.strptime(
        last_week.strftime(format), format)).filter(Log.level == 2).count()

    return {"errors_24h": errors_24h, "warnings_24h": warnings_24h, "errors_7d": errors_7d, "warnings_7d": warnings_7d}
