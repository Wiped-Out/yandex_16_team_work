from abc import ABC, abstractmethod
from flask_sqlalchemy.model import Model


class MainStorage(ABC):
    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass


class BaseSQLAlchemyStorage(MainStorage):
    def get(self, **kwargs):
        pass

    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass


class BaseMainStorage:
    def __init__(self, db: MainStorage, db_model: Model, **kwargs):
        super().__init__(**kwargs)

        self.db = db
        self.model = db_model

    def get_by_id(self, item_id: str):
        pass
