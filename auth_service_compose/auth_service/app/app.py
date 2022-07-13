from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required, current_user

from db.db import init_db, db
from models.models import User
from utils.utils import register_blueprints, register_resources
from typing import Tuple
from flask_restful import Api
from db import cache_db
from services.base_cache import BaseRedisStorage
import redis
from core.settings import settings


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
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    init_db(app)
    init_cache_db()
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app, api


app, api = init_app(__name__)
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route('/', methods=["GET"])
def hello_world():
    return ':)'


@app.route('/happy', methods=["GET"])
@jwt_required()
def happy():
    return render_template('hi.html', title='Hi!', current_user=current_user)


if __name__ == '__main__':
    app.run()
