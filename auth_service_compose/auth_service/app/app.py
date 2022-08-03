from http import HTTPStatus

import flask
import redis
from flask import Flask, render_template, request
from flask_jwt_extended import JWTManager, jwt_required, current_user
from flask_restx import Api
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from sqlalchemy import exc

from core.settings import settings
from db import cache_db, db
from extensions import jwt, flask_restx, flask_migrate, tracer, oauth
from extensions.rate_limiter import rate_limit
from schemas.base.responses import REQUEST_ID_REQUIRED
from services.base_cache import BaseRedisStorage
from services.base_main import BaseSQLAlchemyStorage
from utils.utils import register_blueprints, register_namespaces, log_activity, make_error_response


def init_cache_db():
    cache_db.cache = BaseRedisStorage(
        redis=redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    )


def init_oauth(app: Flask):
    oauth.init_oauth(app)


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


def init_tracer(app: Flask):
    tracer.configure_tracer()
    tracer.Instrumentor = FlaskInstrumentor().instrument_app(app)


def init_migration(app: Flask, sqlalchemy):
    flask_migrate.migrate.init_app(app, sqlalchemy)


def init_app(name: str) -> Flask:
    app = Flask(name)

    register_blueprints(app)

    app.config['SECRET_KEY'] = settings.JWT_PUBLIC_KEY
    app.config['PUBLIC_KEY'] = settings.JWT_PUBLIC_KEY
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.JWT_REFRESH_TOKEN_EXPIRES

    init_api(app=app)
    init_oauth(app=app)

    init_db()
    db.init_sqlalchemy(app=app, storage=db.db)

    init_cache_db()

    init_migration(app=app, sqlalchemy=db.sqlalchemy)

    init_tracer(app=app)

    with app.app_context():
        init_jwt(app=app)

    return app


app = init_app(__name__)


@app.before_request
def before_request_callback():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return make_error_response(msg=REQUEST_ID_REQUIRED,
                                   status=HTTPStatus.BAD_REQUEST)
    if result := rate_limit():
        return result


@app.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    db.sqlalchemy.session.rollback()
    return flask.Response(status=400)


@app.route('/index', methods=["GET"])
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
