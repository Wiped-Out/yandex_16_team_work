import glob
import importlib
import typing
from datetime import datetime
from functools import wraps
from os.path import join

from flask import Flask, current_app, request, Response
from flask_jwt_extended import current_user, get_csrf_token, get_jwt_request_location
from flask_restful import Api

from db.db import sqlalchemy
from models.models import Log, User
from http import HTTPStatus


def save_activity(user: User):
    action = f"{request.method}:{request.url}"
    device = f"{request.user_agent}"
    log = Log(user_id=user.id,
              when=datetime.now(),
              action=action,
              device=device
              )
    sqlalchemy.session.add(log)
    sqlalchemy.session.commit()


def register_blueprints(app: Flask):
    modules = glob.glob(join('views', "*.py"))
    modules = tuple(map(lambda x: x.replace('/', '.'), modules))
    for item in modules:
        if not item.endswith('__init__.py'):
            name = item.split('.')[1]
            module = importlib.import_module(item[:-3])
            app.register_blueprint(getattr(module, f"{name}_view"))


def register_resources(api: Api):
    module = importlib.import_module('urls')
    for url in getattr(module, "urls"):
        api.add_resource(*url)


def handle_csrf():
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if current_user and get_jwt_request_location() == 'cookies':
                token = request.cookies['csrf_access_token']
                request.headers['X-CSRF-TOKEN'] = get_csrf_token(encoded_token=token)
            return func(*args, **kwargs)

        return inner

    return func_wrapper


def work_in_context(app):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with app.app_context():
                return func(*args, **kwargs)

        return inner

    return func_wrapper


def log_activity():
    def func_wrapper(func):
        @wraps(func)
        @work_in_context(current_app)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if not current_user:
                return result
            save_activity(current_user)
            return result

        return inner

    return func_wrapper


def required_role_level(level: int):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if any(role.level >= level for role in current_user.roles):
                return Response(
                    response={'msg': 'Role level is not enough'},
                    status=HTTPStatus.FORBIDDEN,
                    content_type="application/json"
                )
            return func(*args, **kwargs)

        return inner

    return func_wrapper
