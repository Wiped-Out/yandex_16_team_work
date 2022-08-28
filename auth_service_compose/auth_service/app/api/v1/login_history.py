from http import HTTPStatus

from api.v1.__base__ import base_url
from extensions.jwt import jwt_parser
from extensions.pagination import PaginatedResponse, pagination_parser
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from models.models import ActionsEnum, MethodEnum
from schemas.v1 import responses, schemas
from services.logs_service import get_logs_service
from sqlalchemy.exc import IntegrityError
from utils.utils import log_activity, make_error_response

login_history = Namespace('Login history', path=f'{base_url}/users', description='')

_LoginHistory = login_history.model('LoginHistory',
                                    {
                                        'id': fields.String,
                                        'device': fields.String,
                                        'when': fields.DateTime,
                                    },
                                    )

PaginatedLoginHistory = login_history.model('PaginatedLoginHistory',
                                            {
                                                'items': fields.Nested(_LoginHistory, as_list=True),
                                                'total': fields.Integer,
                                                'page': fields.Integer,
                                                'per_page': fields.Integer,
                                            },
                                            )


@login_history.route('/<user_id>/login_history')
@login_history.expect(jwt_parser)
class LoginHistory(Resource):
    @log_activity()
    @jwt_required()
    @login_history.response(code=int(HTTPStatus.OK), description=' ', model=PaginatedLoginHistory)
    @login_history.expect(pagination_parser)
    def get(self, user_id: str):
        logs_service = get_logs_service()

        params = pagination_parser.parse_args()
        page = params['page']
        per_page = params['per_page']
        try:
            answer = logs_service.get_logs(
                user_id=user_id,
                page=page,
                per_page=per_page,
                method=MethodEnum.post,
                action=ActionsEnum.login,
                base_url=request.base_url,
            )
        except IntegrityError:
            return make_error_response(
                msg=responses.WRONG_PARAMS,
                status=HTTPStatus.BAD_REQUEST,
            )

        ans = PaginatedResponse(**answer)
        ans.prepare_items_for_answer(model=schemas.LoginHistory)

        return jsonify(ans.dict())
