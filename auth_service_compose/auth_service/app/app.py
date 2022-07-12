from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required, current_user

from db.db import init_db, db
from models.models import User
from utils.utils import register_blueprints


def init_app(name: str) -> Flask:
    app = Flask(name)
    register_blueprints(app)
    app.config['SECRET_KEY'] = 'secret'
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    init_db(app)
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app


app = init_app(__name__)
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route('/', methods=["GET"])
def hello_world():
    return ':)'


@app.route('/happy', methods=["GET"])
@jwt_required()
def happy():
    return render_template('hi.html', title='Hi!', current_user=current_user)


if __name__ == '__main__':
    app.run()
