import os
from flask import Flask
from ean.database import db
from ean.api import api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ERROR_404_HELP'] = False
    db.init_app(app)
    api.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
