from flask import Blueprint, make_response, redirect, render_template

from extensions.tracer import _trace
from forms.register_form import RegisterForm
from services.user import get_user_service

register_view = Blueprint('register', __name__, template_folder='templates')


@register_view.route('/register', methods=['GET', 'POST'])
@_trace()
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают',
                                   oauth_google_register_url='/oauth2/google/register')
        user_service = get_user_service()
        if user_service.filter_by(
                email=form.email.data, _first=True,
        ) or user_service.filter_by(
            login=form.login.data, _first=True,
        ):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже есть',
                                   oauth_google_register_url='/oauth2/google/register')
        user = user_service.create_user(form.data | {'email_is_confirmed': False})
        user_service.confirm_email_event(user_id=user.id)
        return make_response(redirect('/login'))

    return render_template('register.html', title='Регистрация', form=form,
                           oauth_google_register_url='/oauth2/google/register')
