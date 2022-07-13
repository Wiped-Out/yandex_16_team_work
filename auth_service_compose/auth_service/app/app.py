from typing import Tuple

import redis
from flask import Flask, render_template, request, redirect, jsonify
from flask_jwt_extended import JWTManager, jwt_required, current_user
from flask_restful import Api

from core.settings import settings
from db import cache_db
from db.db import init_db, db
from models.models import User
from services.base_cache import BaseRedisStorage
from utils.utils import register_blueprints, register_resources, log_activity


def init_cache_db():
    cache_db.cache = BaseRedisStorage(
        redis=redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    )


def init_app(name: str) -> Tuple[Flask, Api]:
    app = Flask(name)
    api = Api(app)
    register_blueprints(app)
    register_resources(api)
    app.config['SECRET_KEY'] = 'secret'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    init_db(app)
    init_cache_db()
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app, api


app, api = init_app(__name__)
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    if 'api' not in request.url:
        redir = redirect('/login')
        redir.delete_cookie('session', httponly=True)
        redir.delete_cookie('access_token_cookie', httponly=True)
        return redir

    return jsonify({"msg": "Token has expired"}), 401


@jwt.token_verification_failed_loader
def token_verification_failed_loader_callback(_jwt_header, jwt_data):
    if 'api' not in request.url:
        return redirect('/')
    return jsonify({"msg": "Invalid JWT token"}), 403


@jwt.unauthorized_loader
def unauthorized_loader_callback(explain):
    if 'api' not in request.url:
        return redirect('/')
    return jsonify({"msg": explain}), 401


@jwt.invalid_token_loader
def invalid_token_loader_callback(explain):
    if 'api' not in request.url:
        return redirect('/')
    return jsonify({"msg": explain}), 403


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route('/', methods=["GET"])
@jwt_required(optional=True)
@log_activity()
def hello_world():
    return ':)'


@app.route('/happy', methods=["GET"])
@jwt_required()
@log_activity()
def happy():
    return render_template('hi.html', title='Hi!', current_user=current_user)


if __name__ == '__main__':
    app.run()
