from flask import Flask
from core.settings import settings
from services.base_main import MainStorage, BaseSQLAlchemyStorage
from typing import Optional
from flask_sqlalchemy import SQLAlchemy

db: Optional[MainStorage] = None
sqlalchemy = SQLAlchemy()


def init_sqlalchemy(app: Flask, storage: BaseSQLAlchemyStorage):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{settings.POSTGRES_USER}:' \
        f'{settings.POSTGRES_PASSWORD}@' \
        f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/' \
        f'{settings.POSTGRES_DB}?options=-c%20search_path=content'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    storage.db.init_app(app)

    # with app.app_context():
    # storage.db.create_all()
    # storage.db.session.commit()


def get_db() -> MainStorage:
    return db
