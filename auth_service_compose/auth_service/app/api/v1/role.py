import json
from http import HTTPStatus

import werkzeug.exceptions
from api.v1.__base__ import base_url
from extensions.flask_restx import Namespace
from extensions.jwt import jwt_parser
from extensions.pagination import PaginatedResponse, pagination_parser
from flask import Response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields, reqparse
from schemas.v1 import responses
from schemas.v1.schemas import Role
from services.role import get_role_service
from utils.utils import log_activity

role = Namespace('Role', path=f'{base_url}/roles', description='')

_Role = role.model('Role',
                   {
                       'id': fields.String,
                       'name': fields.String,
                       'level': fields.Integer,
                   },
                   )

NestedRole = role.model('NestedRole',
                        {
                            'items': fields.Nested(_Role, as_list=True),
                        },
                        )

role_parser = reqparse.RequestParser()
role_parser.add_argument('level', type=int, location='json')
role_parser.add_argument('name', type=str, location='json')


@role.route('/')
@role.expect(jwt_parser)
class Roles(Resource):
    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.OK), description=' ', model=NestedRole)
    @role.expect(pagination_parser)
    def get(self) -> Response:
        role_service = get_role_service()

        params = pagination_parser.parse_args()
        page = params['page']
        per_page = params['per_page']

        answer = role_service.get_roles(
            page=page,
            per_page=per_page,
            base_url=request.base_url,
        )

        ans = PaginatedResponse(**answer)
        ans.prepare_items_for_answer(model=Role)

        return jsonify(ans.dict())

    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.CREATED), description=responses.ROLE_CREATED, model=_Role)
    @role.expect(role_parser)
    def post(self) -> Response:
        role_service = get_role_service()
        db_role = role_service.create_role(params=role_parser.parse_args())

        return Response(
            response=Role(**db_role.dict()).json(),
            status=HTTPStatus.CREATED,
            content_type='application/json',
        )


@role.route('/<role_id>')
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
            content_type='application/json',
        )

    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.CREATED), description=' ', model=_Role)
    def get(self, role_id: str) -> Response:
        role_service = get_role_service()

        db_role = role_service.get_role(
            role_id=role_id,
            base_url=request.base_url,
        )

        if not db_role:
            raise werkzeug.exceptions.NotFound(responses.CANT_FIND_ROLE)

        return jsonify(Role(**db_role.dict()).dict())

    @jwt_required()
    @log_activity()
    @role.response(code=int(HTTPStatus.NO_CONTENT), description=responses.ROLE_DELETED)
    def delete(self, role_id: str) -> Response:
        role_service = get_role_service()
        role_service.delete(item_id=role_id)

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT,
            content_type='application/json',
        )
