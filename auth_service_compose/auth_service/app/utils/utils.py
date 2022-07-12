import glob
import importlib
from os.path import join

from flask import Flask


def register_blueprints(app: Flask):
    modules = glob.glob(join('views', "*.py"))
    modules = tuple(map(lambda x: x.replace('/', '.'), modules))
    for item in modules:
        if not item.endswith('__init__.py'):
            name = item.split('.')[1]
            module = importlib.import_module(item[:-3])
            app.register_blueprint(getattr(module, f"{name}_view"))
