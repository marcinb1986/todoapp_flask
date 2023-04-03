import secrets
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import models
from flask_smorest import Api
from resources.actions import blp as ActionsBlueprint
from resources.users import blp as UsersBlueprint
from sqlalchemy import create_engine
import os
import sys
from db import db
from flask_jwt_extended import JWTManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


project_folder = os.path.expanduser(
    '~/OneDrive/Pulpit/todoapp/flask_react/backend')
load_dotenv(os.path.join(project_folder, '.env'))


# from sqlalchemy import MetaData


# db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # replace with your database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = str(
        secrets.SystemRandom().getrandbits(128))
    jwt = JWTManager(app)

    api.register_blueprint(ActionsBlueprint)
    api.register_blueprint(UsersBlueprint)
    # http://127.0.0.1:5000/swagger-ui
    return app


if __name__ == '__main__':

    print("Starting Python web server")
    app.run(debug=True, use_reloader=True)
