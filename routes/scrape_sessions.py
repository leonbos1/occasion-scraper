from flask import Blueprint, jsonify, request
from flask_restful import marshal, fields, abort, Resource
from flask_restful import marshal_with, reqparse

from ..extensions import db

from ..models.scrape_session import ScrapeSession, scrape_session_fields

scrape_sessions = Blueprint("scrape_sessions", __name__)

@scrape_sessions.route("", methods=["GET"])
@marshal_with(scrape_session_fields)
def get_scrape_sessions():
    users = ScrapeSession.query.all()

    return users