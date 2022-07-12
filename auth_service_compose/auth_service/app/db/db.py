from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.settings import settings

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{settings.POSTGRES_USER}:' \
        f'{settings.POSTGRES_PASSWORD}@' \
        f'{settings.POSTGRES_HOST}/' \
        f'{settings.POSTGRES_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
