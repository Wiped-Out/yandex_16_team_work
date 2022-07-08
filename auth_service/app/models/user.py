import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from db.db import db


class User(db.Model, SerializerMixin):
    __table_args__ = {'schema': 'content'}
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'
