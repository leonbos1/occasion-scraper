from flask import Flask
from flask_cors import CORS

from .extensions import url, db

from .routes.cars import cars
from .routes.blueprints import blueprints
from .routes.users import users
from .routes.subscriptions import subscriptions
from .routes.scrape_sessions import scrape_sessions
from .routes.logs import logs
from .routes.catalog import catalog_bp

from .scrape import start, start_blueprint


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
    app.register_blueprint(catalog_bp)

    @app.route("/start", methods=["GET"])
    def index():
        try:
            start()

        except Exception as e:
            return str(e)

        return "Started"

    @app.route("/start/<blueprint_id>", methods=["GET"])
    def start_single_blueprint(blueprint_id):
        try:
            ok = start_blueprint(blueprint_id)
            if not ok:
                return "Blueprint not found", 404
        except Exception as e:
            return str(e), 500

        return "Started"

    @app.route("/api/health", methods=["GET"])
    def health():
        """Health check endpoint for addon monitoring"""
        try:
            # Check database connection
            db.session.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}, 200
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}, 503

    return app
