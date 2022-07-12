import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from db.db import db


class IdMixin(object):
    @declared_attr
    def id(self):
        return db.Column(
            UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
        )


class User(db.Model, IdMixin, SerializerMixin):
    __table_args__ = {"schema": 'content'}
    __tablename__ = "users"

    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    roles = orm.relationship("Role", secondary="UserRole", back_populates="users")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'<User {self.login}>'



class UserIdMixin(object):
    @declared_attr
    def user_id(self):
        return db.Column(UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)


class RefreshToken(db.Model, IdMixin, UserIdMixin, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "refresh_tokens"

    token = db.Column(db.String, nullable=False)
    from_ = db.Column(db.TIMESTAMP, nullable=False)
    to = db.Column(db.TIMESTAMP, nullable=False)


class Log(db.Model, IdMixin, UserIdMixin, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "logs"

    device = db.Column(db.String, nullable=False)
    when = db.Column(db.TIMESTAMP, nullable=False)
    action = db.Column(db.String, nullable=False)


class Role(db.Model, IdMixin, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "roles"

    name = db.Column(db.String, nullable=False)
    level = db.Column(db.INTEGER, nullable=False)

    users = orm.relationship("User", secondary="UserRole", back_populates="roles")


class UserRole(db.Model, IdMixin, SerializerMixin):
    __table_args__ = {"schema": "content"}
    __tablename__ = "user_roles"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Role.id), nullable=False)