from sqlalchemy.orm import relationship

from setup_db import db
from dao.model.genre import Genres

user_fav_movies = db.Table('user_fav_movies',
                           db.Column('id',db.Integer,primary_key=True,autoincrement=True),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
                           )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    role = db.Column(db.String(255))
    favourite_genre = db.Column(db.Integer, db.ForeignKey('genre.id'))
    movie = relationship('Movies',
                         secondary=user_fav_movies,
                         # backref=db.backref('User'),
                         lazy=True,
                         back_populates="user")

