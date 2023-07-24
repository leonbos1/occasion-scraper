from flask import Flask
from flask_cors import CORS

from .extensions import url, db

from .routes.cars import cars

def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(cars, url_prefix="/cars")

    return app