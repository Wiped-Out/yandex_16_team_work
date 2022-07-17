import glob
import importlib
import os
import re
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from os.path import join

from flask import Flask, current_app, request, Response
from flask_jwt_extended import current_user, get_csrf_token, get_jwt_request_location
from flask_restx import Api

from models.models import User
from services.logs_service import get_logs_service


def save_activity(user: User):
    action = f"{request.method}:{request.url}"
    device = f"{request.user_agent}"

    log_service = get_logs_service()

    log_service.create_log(user_id=user.id,
                           when=datetime.now(),
                           action=action,
                           device=device)


def register_blueprints(app: Flask):
    modules = glob.glob(join('views', "*.py"))
    modules = tuple(map(lambda x: x.replace('/', '.'), modules))
    for item in modules:
        if not item.endswith('__init__.py'):
            name = item.split('.')[1]
            module = importlib.import_module(item[:-3])
            app.register_blueprint(getattr(module, f"{name}_view"))


def register_namespaces(api: Api):
    for path in os.walk('api'):
        for module_name in path[2]:
            module_path = f"{path[0]}/{module_name}".replace('/', '.')[:-3]
            if not re.search('__.*__.py', module_name) and re.search("py$", module_name):
                module = importlib.import_module(module_path)
                namespace = getattr(module, module_name[:-3])
                api.add_namespace(namespace)


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


def make_error_response(msg: str, status: int):
    return Response(
        response={'msg': msg},
        status=status,
        content_type="application/json"
    )
