from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.movies import MovieDAO
from dao.user import UserDAO
from service.director import DirectorService
from service.genre import GenreService
from service.movies import MovieService
from service.user import UserService
from setup_db import db

user_dao = UserDAO(db.session)
user_service = UserService(user_dao)

movie_dao = MovieDAO(db.session)
movie_service = MovieService(dao=movie_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(dao=director_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(dao=genre_dao)