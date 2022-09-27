from typing import Optional

from core.settings import settings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
from services.base_main import BaseSQLAlchemyStorage, MainStorage
from services.notify_pipeline import BaseKafkaProducer, MainProducer

db: Optional[MainStorage] = None
sqlalchemy = SQLAlchemy()
notify_pipeline: Optional[MainProducer] = None


def init_sqlalchemy(app: Flask, storage: BaseSQLAlchemyStorage):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}?options=-c%20search_path=content'  # noqa: E501
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    storage.db.init_app(app)


def init_pipeline() -> MainProducer:
    return MainProducer(db=BaseKafkaProducer(
        db_producer=KafkaProducer(
            bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
            api_version=(0, 11, 5))
    ))


def get_db() -> MainStorage:
    if not db:
        raise
    return db


def get_notify_pipeline() -> MainProducer:
    if not notify_pipeline:
        raise
    return notify_pipeline
