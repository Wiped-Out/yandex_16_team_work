import glob
import importlib
from os.path import join
from functools import wraps

from flask import Flask
from flask_restful import Api


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
