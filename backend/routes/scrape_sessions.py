from flask import Blueprint, jsonify
from flask_restful import marshal_with
from collections import defaultdict

from datetime import datetime, timedelta

from ..models.scrape_session import ScrapeSession, scrape_session_fields
from ..models.car import Car

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
        date_obj = session.created
        # Convert datetime object to date string
        if isinstance(date_obj, datetime):
            date = date_obj.strftime('%Y-%m-%d')
        else:
            # If it's already a string, parse it
            try:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
            except:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

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


@scrape_sessions.route("/best_days")
def get_best_days():
    """
    Returns top 10 most successful days based on amount of cars scraped
    """
    sessions = ScrapeSession.query.all()

    cars_per_day = {}

    for session in sessions:
        date_obj = session.created
        # Convert datetime object to date string
        if isinstance(date_obj, datetime):
            date = date_obj.strftime('%Y-%m-%d')
        else:
            # If it's already a string, parse it
            try:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
            except:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        if not session.new_cars:
            continue

        if date in cars_per_day:
            cars_per_day[date] += session.new_cars
        else:
            cars_per_day[date] = session.new_cars

    cars_per_day_list = [{'date': date, 'cars': cars}
                         for date, cars in cars_per_day.items()]

    cars_per_day_list.sort(
        key=lambda x: x['cars'], reverse=True)

    return jsonify(cars_per_day_list[:10])


@scrape_sessions.route("/cars_per_week/<int:weeks>", methods=["GET"])
def get_cars_per_week(weeks):
    """
    Returns the amount of cars scraped per week for the last x weeks
    """
    sessions = ScrapeSession.query.filter(ScrapeSession.created > (
        datetime.now() - timedelta(weeks=weeks))).all()

    cars_per_week = defaultdict(int)

    for session in sessions:
        date_obj = session.created
        # Convert datetime object or parse string
        if isinstance(date_obj, datetime):
            date = date_obj
        else:
            try:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S')

        if not session.new_cars:
            continue

        week_number = date.isocalendar()[1]

        cars_per_week[week_number] += session.new_cars

    cars_per_week_list = [{'week_number': week, 'cars': cars}
                          for week, cars in cars_per_week.items()]

    cars_per_week_list.sort(key=lambda x: x['week_number'])

    current_week_number = datetime.now().isocalendar()[1]

    max_week_numer = current_week_number - weeks

    cars_per_week_list = [
        week for week in cars_per_week_list if week['week_number'] >= max_week_numer]

    return jsonify(cars_per_week_list)


@scrape_sessions.route("/cars_per_month/<int:months>", methods=["GET"])
def get_cars_per_month(months):
    """
    Returns the amount of cars scraped per month for the last x months
    """
    sessions = ScrapeSession.query.filter(ScrapeSession.created > (
        datetime.now() - timedelta(days=months*30))).all()

    cars_per_months = defaultdict(int)

    for session in sessions:
        date_obj = session.created
        # Convert datetime object or parse string
        if isinstance(date_obj, datetime):
            date = date_obj
        else:
            try:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                date = datetime.strptime(
                    date_obj, '%Y-%m-%d %H:%M:%S')

        if not session.new_cars:
            continue

        month_name = date.strftime("%B")

        cars_per_months[month_name] += session.new_cars

    cars_per_month_list = [{'month': month, 'cars': cars}
                           for month, cars in cars_per_months.items()]

    cars_per_month_list.sort(key=lambda x: x['month'])

    current_month_index = datetime.now().month

    max_month_index = current_month_index - months

    cars_per_month_list = [
        month for month in cars_per_month_list if datetime.strptime(month['month'], '%B').month >= max_month_index]

    cars_per_month_list.sort(
        key=lambda x: datetime.strptime(x['month'], '%B').month)

    return jsonify(cars_per_month_list)