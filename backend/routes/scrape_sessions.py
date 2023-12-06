from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from datetime import datetime, timedelta

from ..models.scrape_session import ScrapeSession, scrape_session_fields

scrape_sessions = Blueprint("scrape_sessions", __name__)


@scrape_sessions.route("", methods=["GET"])
@marshal_with(scrape_session_fields)
def get_scrape_sessions():
    users = ScrapeSession.query.all()

    return users

# endpoints for getting the amount of cars scraped per day for the last x days


@scrape_sessions.route("/cars_per_day/<int:days>", methods=["GET"])
def get_cars_per_day(days):
    # scrape_sessions.created is like 2023-11-19 13:05:00.291988
    sessions = ScrapeSession.query.filter(ScrapeSession.created > (
        datetime.now() - timedelta(days=days))).all()

    cars_per_day = {}

    for session in sessions:
        date_string = session.created
        try:
            date = datetime.strptime(
                date_string, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
        except:
            date = datetime.strptime(
                date_string, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        if not session.new_cars:
            continue

        if date in cars_per_day:
            cars_per_day[date] += session.new_cars
        else:
            cars_per_day[date] = session.new_cars

    cars_per_day_list = [{'date': date, 'cars': cars}
                         for date, cars in cars_per_day.items()]
    
    cars_per_day_list.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

    return jsonify(cars_per_day_list)
