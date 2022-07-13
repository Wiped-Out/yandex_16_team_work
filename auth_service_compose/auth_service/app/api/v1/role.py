from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.role import get_role_service
from flask import jsonify
from flask import current_app
from utils.utils import work_in_context


class Role(Resource):
    @jwt_required()
    @work_in_context(current_app)
    def delete(self, role_id: str):
        role_service = get_role_service()
        role_service.delete_role(role_id=role_id)

    @jwt_required()
    def put(self, role_id: str, body: dict):
        # todo
        pass

    @jwt_required()
    def post(self, body: dict):
        # todo
        pass

    @jwt_required()
    @work_in_context(current_app)
    def get(self, role_id: str):
        role_service = get_role_service()

        # todo формировать по юрлу
        cache_key = f"d;fja;sf{role_id}"

        return jsonify(role_service.get_role(role_id=role_id, cache_key=cache_key))
