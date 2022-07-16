from datetime import timedelta, datetime, timezone
from typing import Tuple

import flask
import redis
from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required, current_user, get_jwt, set_access_cookies
from flask_restful import Api
from flask_migrate import Migrate
from sqlalchemy import exc

from core.settings import settings
from db import cache_db, db
from extensions import jwt
from services.base_cache import BaseRedisStorage
from services.base_main import BaseSQLAlchemyStorage
from services.jwt import get_jwt_service
from utils.utils import register_blueprints, register_resources, log_activity


def init_cache_db():
    cache_db.cache = BaseRedisStorage(
        redis=redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    )


def init_db():
    db.db = BaseSQLAlchemyStorage(db=db.sqlalchemy)


def init_jwt(app: Flask):
    jwt.jwt_manager = JWTManager(app)
    jwt.set_jwt_callbacks()


def init_app(name: str) -> Tuple[Flask, Api]:
    app = Flask(name)
    api = Api(app)
    register_blueprints(app)
    register_resources(api)
    app.config['SECRET_KEY'] = 'secret'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.JWT_REFRESH_TOKEN_EXPIRES

    init_db()
    db.init_sqlalchemy(app=app, storage=db.db)
    init_cache_db()

    migrate = Migrate(app, db.sqlalchemy)

    with app.app_context():
        init_jwt(app)

    return app, api


app, api = init_app(__name__)


@app.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    db.sqlalchemy.session.rollback()
    return flask.Response(status=400)


@app.route('/', methods=["GET"])
@jwt_required(optional=True)
@log_activity()
def index():
    return render_template('base.html', title='Главная', current_user=current_user)


@app.route('/happy', methods=["GET"])
@jwt_required()
@log_activity()
def happy():
    return render_template('hi.html', title='Hi!', current_user=current_user)


if __name__ == '__main__':
    app.run()
