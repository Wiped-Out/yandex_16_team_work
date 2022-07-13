from datetime import timedelta

from flask import render_template, redirect, Blueprint, current_app
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required

from forms.login_form import LoginForm
from models.models import User
from utils.utils import log_activity, handle_csrf

login_view = Blueprint('login', __name__, template_folder='templates')


@login_view.route('/login', methods=['GET', 'POST'])
@jwt_required(optional=True)
@log_activity()
@handle_csrf()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with current_app.app_context():
            user = User.query.filter_by(login=form.login.data).first()

            if user and user.check_password(form.password.data):
                token = create_access_token(identity=user, expires_delta=timedelta(seconds=10))
                response = redirect("/happy")
                set_access_cookies(response, token)
                return response

            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, title='Авторизация')

    return render_template('login.html', title='Авторизация', form=form)
