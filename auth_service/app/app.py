from flask import Flask

from db.db import init_db, db
from models.user import User


def init_app(name: str) -> Flask:
    app = Flask(name)
    init_db(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app


app = init_app(__name__)


@app.route('/hello-world')
def hello_world():
    with app.app_context():
        return str(User.query.all())


if __name__ == '__main__':
    app.run()
