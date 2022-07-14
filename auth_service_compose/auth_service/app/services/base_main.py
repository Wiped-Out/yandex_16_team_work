from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy


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


class BaseSQLAlchemyStorage(MainStorage):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get(self, item_id: str, model, **kwargs):
        return model.query.filter(model.id == item_id).first()

    def create(self, model, **kwargs):
        item = model(**kwargs)
        self.add(item)
        self.commit()
        return item

    def update(self, item_id: str, model, **kwargs):
        model.query.filter_by(id=item_id).update(kwargs)
        self.commit()

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

    def create(self, **kwargs):
        return self.db.create(model=self.model, **kwargs)

    def update(self, item_id: str, **kwargs):
        return self.db.update(item_id=item_id, model=self.model, **kwargs)

    def get_all(self, **kwargs):
        return self.db.get_all(model=self.model, **kwargs)
