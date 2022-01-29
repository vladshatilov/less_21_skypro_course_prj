from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api

from config import Config
from dao.model.movies import Movies
from dao.model.user import User
from setup_db import db
from views.director import directors_ns
from views.genre import genres_ns
from views.movies import movies_ns
from views.user import user_ns


def create_app(config_object):
    app = Flask(__name__)

    CORS(app)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    api.add_namespace(user_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
#     create_data(app,db)
#
# def create_data(app,db):
#     with app.app_context():
        # db.drop_all()
        # db.create_all()
        # u1 = User(name="adnerew", password="my_little_pony", role="user")
        # # c1 = Movies.query.get(1)
        # # u1.movie.append(c1)
        # # db.session.add(matrix)
        # # db.session.commit()
        # u2 = User(name="vlad", password="qwerty", role="user")
        # u3 = User(name="admin", password="admin", role="admin")
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()
        # with db.session.begin():
        #     db.session.add_all([u1,u2,u3])


app = create_app(Config())


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
