from flask_restful import Resource
from flask_jwt_extended import jwt_required
from schemas.schemas import Role
from flask import jsonify, current_app, request, Response
from services.role import get_role_service
from utils.utils import work_in_context


class Roles(Resource):
    @jwt_required()
    @work_in_context(current_app)
    def get(self) -> Response:
        role_service = get_role_service()
        cache_key = request.base_url

        db_roles = role_service.get_roles(cache_key=cache_key)
        return jsonify([Role(**role.dict()).dict() for role in db_roles])
