from flask_restful import Resource
from flask_jwt_extended import jwt_required
from schemas.schemas import Role
from flask import jsonify, Response
from services.role import get_role_service
from utils.utils import work_in_context
from flask import current_app


class Roles(Resource):
    @jwt_required()
    @work_in_context(current_app)
    def get(self) -> Response:
        role_service = get_role_service()

        # todo создавать cache_key на основе юрла
        cache_key = "afj;asfjs;af"

        return jsonify([Role(**role.dict()).dict() for role in role_service.get_roles(cache_key=cache_key)])
