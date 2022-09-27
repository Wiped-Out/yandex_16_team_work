from extensions.tracer import _trace
from flask import Blueprint, make_response, redirect
from services.user import get_user_service

confirm_view = Blueprint('confirm', __name__, template_folder='templates')


@confirm_view.route('/confirm/<confirm_id>/email', methods=['GET'])
@_trace()
def confirm_email(confirm_id: str):
    user_service = get_user_service()
    if user_service.confirm_email(confirm_id=confirm_id):
        return make_response(redirect('/login'))
    return make_response(redirect('/index'))
