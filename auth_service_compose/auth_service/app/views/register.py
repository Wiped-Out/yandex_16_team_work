from flask import render_template, redirect, Blueprint, current_app

from db.db import db
from forms.register_form import RegisterForm
from models.models import User

register_view = Blueprint('register', __name__, template_folder='templates')


@register_view.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        with current_app.app_context():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")

            if User.query.filter_by(email=form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                email=form.email.data,
                login=form.login.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)
