from flask_restful import Resource
from services.role import get_role_service
from flask import jsonify, request, Response
from schemas import schemas
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from utils.utils import log_activity
from flask_restful import reqparse


class Role(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('level', type=int)
        self.parser.add_argument('name', type=str)

    @jwt_required()
    @log_activity()
    def delete(self, role_id: str) -> Response:
        role_service = get_role_service()
        role_service.delete(item_id=role_id)

        return Response(status=HTTPStatus.NO_CONTENT)

    @jwt_required()
    @log_activity()
    def put(self, role_id: str) -> Response:
        role_service = get_role_service()

        role_service.update_role(role_id=role_id, body=self.parser.parse_args())

        return Response(status=HTTPStatus.NO_CONTENT)

    @jwt_required()
    @log_activity()
    def post(self) -> Response:
        role_service = get_role_service()
        db_role = role_service.create_role(body=self.parser.parse_args())

        return Response(
            schemas.Role(**db_role.dict()).json(),
            status=HTTPStatus.CREATED,
            content_type="application/json"
        )

    @jwt_required()
    @log_activity()
    def get(self, role_id: str) -> Response:
        role_service = get_role_service()
        cache_key = request.base_url

        db_role = role_service.get_role(role_id=role_id, cache_key=cache_key)
        return jsonify(schemas.Role(**db_role.dict()).dict())
