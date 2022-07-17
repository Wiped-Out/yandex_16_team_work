from http import HTTPStatus

from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields, Namespace

from api.v1.__base__ import base_url
from extensions.jwt import jwt_parser
from schemas.v1.schemas import Role
from services.role import get_role_service
from utils.utils import log_activity

roles = Namespace('Roles', path=f"{base_url}/roles", description='')

_Role = roles.model("Role",
                    {
                        "id": fields.String,
                        "name": fields.String,
                        "level": fields.Integer
                    }
                    )


@roles.route("/")
@roles.expect(jwt_parser)
class Roles(Resource):
    @jwt_required()
    @log_activity()
    @roles.response(code=int(HTTPStatus.OK), description=" ", model=[_Role])
    def get(self) -> Response:
        role_service = get_role_service()
        cache_key = request.base_url

        db_roles = role_service.get_roles(cache_key=cache_key)
        return jsonify([Role(**role.dict()).dict() for role in db_roles])
