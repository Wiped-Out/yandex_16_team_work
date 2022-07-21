import json
from http import HTTPStatus

from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required
from flask_restx import Resource, reqparse, fields

from api.v1.__base__ import base_url
from extensions.flask_restx import Namespace
from extensions.jwt import jwt_parser
from schemas.v1 import schemas
from services.role import get_role_service
from utils.utils import log_activity
from schemas.v1.schemas import Role
from api.responses import responses

role = Namespace('Role', path=f"{base_url}/roles", description='')

_Role = role.model("Role",
                   {
                       "id": fields.String,
                       "name": fields.String,
                       "level": fields.Integer
                   }
                   )

NestedRole = role.model("NestedRole",
                        {
                            "items": fields.Nested(_Role, as_list=True)
                        })

role_parser = reqparse.RequestParser()
role_parser.add_argument('level', type=int, location='json')
role_parser.add_argument('name', type=str, location='json')


@role.route("/")
@role.expect(jwt_parser)
class Roles(Resource):
    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.OK), description=" ", model=NestedRole)
    def get(self) -> Response:
        role_service = get_role_service()
        cache_key = request.base_url

        db_roles = role_service.get_roles(cache_key=cache_key)
        return jsonify(
            {"items": [Role(**db_role.dict()).dict() for db_role in db_roles]}
        )

    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.CREATED), description=responses.ROLE_CREATED, model=_Role)
    @role.expect(role_parser)
    def post(self) -> Response:
        role_service = get_role_service()
        db_role = role_service.create_role(params=role_parser.parse_args())

        return Response(
            response=schemas.Role(**db_role.dict()).json(),
            status=HTTPStatus.CREATED,
            content_type="application/json"
        )


@role.route("/<role_id>")
@role.expect(jwt_parser)
class RoleId(Resource):
    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.NO_CONTENT), description=responses.ROLE_CREATED)
    @role.expect(role_parser)
    def put(self, role_id: str) -> Response:
        role_service = get_role_service()
        role_service.update_role(
            role_id=role_id,
            params=role_parser.parse_args(),
        )

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT,
            content_type="application/json"
        )

    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.CREATED), description=" ", model=_Role)
    def get(self, role_id: str) -> Response:
        role_service = get_role_service()
        cache_key = request.base_url

        db_role = role_service.get_role(role_id=role_id, cache_key=cache_key)
        return jsonify(schemas.Role(**db_role.dict()).dict())

    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.NO_CONTENT), description=responses.ROLE_DELETED)
    def delete(self, role_id: str) -> Response:
        role_service = get_role_service()
        role_service.delete(item_id=role_id)

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT,
            content_type="application/json"
        )
