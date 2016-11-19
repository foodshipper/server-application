from flask import Flask

from api import api
from database import create_tables


def create_app():
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    api.init_app(app)
    create_tables()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
