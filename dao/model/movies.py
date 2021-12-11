from marshmallow import Schema, fields
from sqlalchemy.orm import relationship

from dao.model.user import user_fav_movies
from setup_db import db


class Movies(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    trailer = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    genre = db.relationship('Genres')
    director = db.relationship('Directors')
    user = relationship('User',
                        secondary=user_fav_movies,
                        # backref='Movies',
                        lazy=True,
                        back_populates="movie")


class Usefull_scheme(Schema):
    pk = fields.Integer()
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()
    email = fields.String()
    password = fields.String()
    name = fields.String()
    surname = fields.String()
    role = fields.String()
    access_token = fields.String()
    refresh_token = fields.String()
    genre_name = fields.String()
    director_name = fields.String()
    favourite_genre = fields.Integer()
