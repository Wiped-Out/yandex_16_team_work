import flask
import redis
from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required, current_user
from flask_migrate import Migrate
from flask_restx import Api
from sqlalchemy import exc

from core.settings import settings
from db import cache_db, db
from extensions import jwt, flask_restx
from services.base_cache import BaseRedisStorage
from services.base_main import BaseSQLAlchemyStorage
from utils.utils import register_blueprints, register_namespaces, log_activity


def init_cache_db():
    cache_db.cache = BaseRedisStorage(
        redis=redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    )


def init_db():
    db.db = BaseSQLAlchemyStorage(db=db.sqlalchemy)


def init_jwt(app: Flask):
    jwt.jwt_manager = JWTManager(app)
    jwt.set_jwt_callbacks()


def init_api(app: Flask):
    flask_restx.api = Api(app,
                          doc=f"/{settings.API_URL}/docs",
                          base_url=f"/{settings.API_URL}",
                          authorizations=flask_restx.authorizations)
    register_namespaces(flask_restx.api)


def init_app(name: str) -> Flask:
    app = Flask(name)

    register_blueprints(app)

    app.config['SECRET_KEY'] = 'secret'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.JWT_REFRESH_TOKEN_EXPIRES

    init_api(app)
    init_db()
    db.init_sqlalchemy(app=app, storage=db.db)
    init_cache_db()

    migrate = Migrate(app, db.sqlalchemy)

    with app.app_context():
        init_jwt(app)

    return app


app = init_app(__name__)


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
