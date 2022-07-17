from typing import Type

from flask_restx import Resource

from api.v1.jwt_tokens import JWTLogin, JWTLogout, JWTRefresh
from api.v1.role import Role
from api.v1.roles import Roles
from api.v1.user import User
from api.v1.login_history import LoginHistory


class URL:
    def __init__(self, resource: Type[Resource], *urls):
        self.resource = resource
        self.urls = urls

    def __iter__(self):
        return iter((self.resource, *self.urls))


urls = [
    URL(Role, "/api/v1/role", "/api/v1/role/<role_id>"),
    URL(Roles, "/api/v1/roles"),
    URL(User, "/api/v1/user", "/api/v1/user/<user_id>"),
    URL(LoginHistory, "/api/v1/user/<user_id>/login_history"),
    URL(JWTLogin, "/api/v1/login"),
    URL(JWTLogout, "/api/v1/logout"),
    URL(JWTRefresh, "/api/v1/refresh"),
]
