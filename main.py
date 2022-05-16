from flask import Flask
from flask_restx import Api

from app.config import Config
from app.database import db
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns


def create_app(config: Config):
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)


def load_data():
    db.create_all()


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    load_data()
    app.run()
