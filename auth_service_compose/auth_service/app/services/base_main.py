from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query


class AdditionalActions(str, Enum):
    _sort_by = "_sort_by"
    _first = "_first"


def sqalchemy_additional_actions():
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            actions = {item.value: kwargs.pop(item.value) if item.value in kwargs and item.value else None
                       for item in AdditionalActions}
            result: Query = func(*args, **kwargs)
            model = kwargs["model"]
            if value := actions[AdditionalActions._sort_by]:
                if value.startswith("-"):
                    result.order_by(getattr(model, value).desc())
                else:
                    result.order_by(getattr(model, value))
            if value := actions[AdditionalActions._first]:
                result = result.first()
            return result

        return inner

    return func_wrapper


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

    @abstractmethod
    def commit(self, **kwargs):
        pass

    @abstractmethod
    def add(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass

    @abstractmethod
    def get_all(self, **kwargs):
        pass

    @abstractmethod
    def filter_by(self, **kwargs):
        pass

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass


class BaseSQLAlchemyStorage(MainStorage):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get(self, item_id: str, model, **kwargs):
        return model.query.get(item_id)

    def create(self, model, need_commit: bool = True, **kwargs):
        item = model(**kwargs)
        self.add(item)

        if need_commit:
            self.commit()
        return item

    def update(self, item_id: str, model, **kwargs):
        model.query.filter_by(id=item_id).update(kwargs)
        self.commit()

    @sqalchemy_additional_actions()
    def filter_by(self, model, **kwargs):
        return model.query.filter_by(**kwargs)

    @sqalchemy_additional_actions()
    def filter(self, model, *args, **kwargs):
        return model.query.filter(*args)

    def commit(self, **kwargs):
        return self.db.session.commit(**kwargs)

    def add(self, *args, **kwargs):
        return self.db.session.add(*args)

    def delete(self, item_id: str, model, **kwargs):
        model.query.filter_by(id=item_id).delete()
        self.commit()

    def get_all(self, model, **kwargs):
        return model.query.all()


class BaseMainStorage:
    def __init__(self, db: MainStorage, db_model, **kwargs):
        super().__init__(**kwargs)

        self.db = db
        self.model = db_model

    def get(self, item_id: str):
        return self.db.get(item_id=item_id, model=self.model)

    def delete(self, item_id: str):
        return self.db.delete(item_id=item_id, model=self.model)

    def filter_by(self, _first=None, _sort_by=None, **kwargs):
        return self.db.filter_by(model=self.model, _first=_first, **kwargs)

    def filter(self, _first=None, _sort_by=None, *args, **kwargs):
        return self.db.filter(model=self.model, _first=_first, *args)

    def create(self, **kwargs):
        return self.db.create(model=self.model, **kwargs)

    def update(self, item_id: str, **kwargs):
        return self.db.update(item_id=item_id, model=self.model, **kwargs)

    def get_all(self, **kwargs):
        return self.db.get_all(model=self.model, **kwargs)
