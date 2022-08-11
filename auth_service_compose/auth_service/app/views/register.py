from flask import render_template, redirect, Blueprint, make_response

from extensions.tracer import _trace
from forms.register_form import RegisterForm
from services.user import get_user_service

register_view = Blueprint('register', __name__, template_folder='templates')


@register_view.route('/register', methods=['GET', 'POST'])
@_trace()
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   oauth_google_register_url='/oauth2/google/register')
        user_service = get_user_service()
        if user_service.filter_by(email=form.email.data, _first=True) or \
                user_service.filter_by(login=form.login.data, _first=True):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   oauth_google_register_url='/oauth2/google/register')
        user_service.create_user(form.data)
        return make_response(redirect('/login'))

    return render_template('register.html', title='Регистрация', form=form,
                           oauth_google_register_url='/oauth2/google/register')
