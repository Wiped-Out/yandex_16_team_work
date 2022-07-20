import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from db.db import sqlalchemy


class IdMixin(object):
    @declared_attr
    def id(self):
        return sqlalchemy.Column(
            UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
        )


user_roles = sqlalchemy.Table(
    "user_roles",
    sqlalchemy.metadata,
    sqlalchemy.Column("user_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("role_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("roles.id"), nullable=False),
)


class User(sqlalchemy.Model, IdMixin, SerializerMixin):
    __tablename__ = "users"

    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    roles = sqlalchemy.relation(
        "Role",
        secondary=user_roles,
        back_populates="users"
    )

    logs = sqlalchemy.relation("Log")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.login}>'


class UserIdMixin(object):
    @declared_attr
    def user_id(self):
        return sqlalchemy.Column(UUID(as_uuid=True), sqlalchemy.ForeignKey(User.id), nullable=False)


class RefreshToken(sqlalchemy.Model, IdMixin, UserIdMixin, SerializerMixin):
    __tablename__ = "refresh_tokens"

    token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    from_ = sqlalchemy.Column(sqlalchemy.TIMESTAMP, nullable=False)
    to = sqlalchemy.Column(sqlalchemy.TIMESTAMP, nullable=False)


class Log(sqlalchemy.Model, IdMixin, UserIdMixin, SerializerMixin):
    __tablename__ = "logs"

    device = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    when = sqlalchemy.Column(sqlalchemy.TIMESTAMP, nullable=False)
    action = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Role(sqlalchemy.Model, IdMixin, SerializerMixin):
    __tablename__ = "roles"

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    level = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=False)

    users = sqlalchemy.relation(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )
