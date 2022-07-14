from flask_restful import Resource
from services.logs_service import get_logs_service
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from utils.utils import log_activity
from schemas import schemas


class LoginHistory(Resource):
    @log_activity()
    @jwt_required()
    def get(self, user_id: str):
        logs_service = get_logs_service()

        logs = logs_service.get_logs(
            cache_key=request.base_url,
            user_id=user_id,
            pattern="POST:.*login.*"
        )
        return jsonify([schemas.LoginHistory(**log.dict()).dict() for log in logs])
