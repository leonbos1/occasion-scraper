from flask import Blueprint, jsonify
from flask_restful import marshal_with
from collections import defaultdict

from datetime import datetime, timedelta

from ..models.scrape_session import ScrapeSession, scrape_session_fields

scrape_sessions = Blueprint("scrape_sessions", __name__)


@scrape_sessions.route("", methods=["GET"])
@marshal_with(scrape_session_fields)
def get_scrape_sessions():
    users = ScrapeSession.query.all()

    return users


@scrape_sessions.route("/cars_per_day/<int:days>", methods=["GET"])
def get_cars_per_day(days):
    """
    Returns the amount of cars scraped per day for the last x days
    """
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

    cars_per_day_list.sort(
        key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

    return jsonify(cars_per_day_list)


@scrape_sessions.route("/cars_per_week/<int:weeks>", methods=["GET"])
def get_cars_per_week(weeks):
    """
    Returns the amount of cars scraped per week for the last x weeks
    """
    sessions = ScrapeSession.query.filter(ScrapeSession.created > (
        datetime.now() - timedelta(weeks=weeks))).all()

    cars_per_week = defaultdict(int)

    for session in sessions:
        date_string = session.created
        try:
            date = datetime.strptime(
                date_string, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            date = datetime.strptime(
                date_string, '%Y-%m-%d %H:%M:%S')

        if not session.new_cars:
            continue

        # Get week number of the year
        week_number = date.isocalendar()[1]

        cars_per_week[week_number] += session.new_cars

    cars_per_week_list = [{'week_number': week, 'cars': cars}
                          for week, cars in cars_per_week.items()]

    # Sorting the list based on the week number
    cars_per_week_list.sort(key=lambda x: x['week_number'])

    # get the last weeks amount of cars
    current_week_number = datetime.now().isocalendar()[1]

    max_week_numer = current_week_number - weeks

    cars_per_week_list = [
        week for week in cars_per_week_list if week['week_number'] >= max_week_numer]

    return jsonify(cars_per_week_list)
