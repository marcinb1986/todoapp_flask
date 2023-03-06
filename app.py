from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import models
from flask_smorest import Api
# from sqlalchemy import MetaData
from resources.actions import blp as ActionsBlueprint
from sqlalchemy import create_engine


db = SQLAlchemy()


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
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ActionsBlueprint)
    # http://127.0.0.1:5000/swagger-ui
    return app


if __name__ == '__main__':

    print("Starting Python web server")
    app.run(debug=True, use_reloader=True)
