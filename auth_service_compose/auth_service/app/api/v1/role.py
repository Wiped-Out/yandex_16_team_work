from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.role import get_role_service
from flask import jsonify, current_app, request, Response
from utils.utils import work_in_context
from schemas import schemas
from http import HTTPStatus


class Role(Resource):
    @jwt_required()
    @work_in_context(current_app)
    def delete(self, role_id: str) -> Response:
        role_service = get_role_service()
        role_service.delete_role(role_id=role_id)

        return Response(status=HTTPStatus.NO_CONTENT)

    @jwt_required()
    @work_in_context(current_app)
    def put(self, role_id: str) -> Response:
        role_service = get_role_service()

        role_service.update_role(role_id=role_id, body=request.json)

        return Response(status=HTTPStatus.OK)

    @jwt_required()
    @work_in_context(current_app)
    def post(self) -> Response:
        role_service = get_role_service()
        db_role = role_service.create_role(body=request.json)

        return Response(
            schemas.Role(**db_role.dict()).json(),
            status=HTTPStatus.CREATED,
            content_type="application/json"
        )

    @jwt_required()
    @work_in_context(current_app)
    def get(self, role_id: str) -> Response:
        role_service = get_role_service()
        cache_key = request.base_url

        db_role = role_service.get_role(role_id=role_id, cache_key=cache_key)
        return jsonify(schemas.Role(**db_role.dict()).dict())
