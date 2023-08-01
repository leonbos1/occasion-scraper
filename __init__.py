from flask import Flask
from flask_cors import CORS

from .extensions import url, db

from .routes.cars import cars
from .routes.blueprints import blueprints
from .routes.users import users
from .routes.subscriptions import subscriptions
from .routes.scrape_sessions import scrape_sessions
from .routes.logs import logs

from .scrape import start

def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(cars, url_prefix="/cars")
    app.register_blueprint(blueprints, url_prefix="/blueprints")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(subscriptions, url_prefix="/subscriptions")
    app.register_blueprint(scrape_sessions, url_prefix="/scrape_sessions")
    app.register_blueprint(logs, url_prefix="/logs")

    @app.route("/start", methods=["GET"])
    def index():
        start()

    return app