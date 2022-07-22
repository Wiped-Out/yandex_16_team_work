from flask import render_template, redirect, Blueprint, make_response
from flask_jwt_extended import set_access_cookies, jwt_required, set_refresh_cookies

from extensions.tracer import _trace
from forms.login_form import LoginForm
from services.jwt import get_jwt_service
from services.user import get_user_service
from utils.utils import log_activity, handle_csrf, save_activity

login_view = Blueprint('login', __name__, template_folder='templates')


@login_view.route('/login', methods=['GET', 'POST'])
@jwt_required(optional=True)
@log_activity()
@handle_csrf()
@_trace()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        jwt_service = get_jwt_service()
        user_service = get_user_service()
        user = user_service.filter_by(login=form.login.data, _first=True)
        if user and user.check_password(form.password.data):
            refresh_token = jwt_service.create_refresh_token(user=user)

            token = jwt_service.create_access_token(user=user)

            response = make_response(redirect("/happy"))

            set_access_cookies(response, token)
            set_refresh_cookies(response, refresh_token)

            save_activity(user)
            return response

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')

    return render_template('login.html', title='Авторизация', form=form)
