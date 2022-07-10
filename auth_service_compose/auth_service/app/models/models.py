import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from db.db import db


class IdMixin(object):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class User(IdMixin, db.Model, SerializerMixin):
    __table_args__ = {"schema": 'content'}
    __tablename__ = "users"

    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'


class UserIdMixin(object):
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)


class RefreshToken(IdMixin, UserIdMixin, db.Model, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "refresh_tokens"

    token = db.Column(db.String, nullable=False)
    from_ = db.Column(db.TIMESTAMP, nullable=False)
    to = db.Column(db.TIMESTAMP, nullable=False)


class Log(IdMixin, UserIdMixin, db.Model, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "logs"

    device = db.Column(db.String, nullable=False)
    when = db.Column(db.TIMESTAMP, nullable=False)
    action = db.Column(db.String, nullable=False)


class Role(IdMixin, UserIdMixin, db.Model, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "roles"

    name = db.Column(db.String, nullable=False)
    level = db.Column(db.INTEGER, nullable=False)


class UserRole(IdMixin, db.Model, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "user_roles"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Role.id), nullable=False)
