import glob
import importlib
from datetime import datetime
from functools import wraps
from os.path import join

from flask import Flask, current_app, request
from flask_jwt_extended import current_user
from flask_restful import Api

from db.db import db
from models.models import Log


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
            action = f"{request.method}:{request.url}"
            device = f"{request.user_agent}"
            log = Log(user_id=current_user.id,
                      when=datetime.now(),
                      action=action,
                      device=device
                      )
            db.session.add(log)
            db.session.commit()
            return result

        return inner

    return func_wrapper
