from http import HTTPStatus

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace
from flask_restx import fields

from api.v1.__base__ import base_url
from extensions.jwt import jwt_parser
from schemas.v1 import schemas
from services.logs_service import get_logs_service
from utils.utils import log_activity

login_history = Namespace('Login history', path=f"{base_url}/users", description='')

_LoginHistory = login_history.model("LoginHistory",
                                    {
                                        "id": fields.String,
                                        "device": fields.String,
                                        "when": fields.DateTime
                                    }
                                    )


@login_history.route('/<user_id>/login_history')
@login_history.expect(jwt_parser)
class LoginHistory(Resource):
    @log_activity()
    @jwt_required()
    @login_history.response(code=int(HTTPStatus.OK), description=" ", model=_LoginHistory)
    def get(self, user_id: str):
        logs_service = get_logs_service()

        logs = logs_service.get_logs(
            cache_key=request.base_url,
            user_id=user_id,
            pattern="POST:.*login.*"
        )
        return jsonify(
            {"items": [schemas.LoginHistory(**log.dict()).dict() for log in logs]}
        )
