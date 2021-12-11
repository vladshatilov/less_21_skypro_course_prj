from flask import request
from sqlalchemy import desc

from dao.model.director import Directors
from dao.model.genre import Genres
from dao.model.movies import Movies


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        movies = self.session.query(Movies.id, Movies.title, Movies.year,
                                    Movies.description, Movies.trailer,
                                    Movies.genre_id,
                                    Genres.name.label('genre_name'),
                                    Movies.rating,
                                    Movies.director_id
                                    , Directors.name.label('director_name')
                                    ).join(Genres, Movies.genre_id == Genres.id) \
            .join(Directors, Movies.director_id == Directors.id).filter(
            (Movies.year == request.args.get('year') if request.args.get('year') is not None else 1 == 1),
            (Genres.id == request.args.get('genre_id') if request.args.get('genre_id') is not None else 1 == 1),
            (Directors.id == request.args.get('director_id') if request.args.get('director_id') is not None else 1 == 1)
        )
        if (request.args.get('status') is not None and request.args.get('status') == 'new'):
            movies = movies.order_by(desc(Movies.year), Movies.title)
        try:
            if request.args.get('page_size') is not None and request.args.get('page_size').isdigit() and 0 < int(request.args.get('page_size')) < 200:
                page_size = int(request.args.get('page_size'), 10)
                movies = movies.limit(page_size)
            if request.args.get('page') is not None and request.args.get('page').isdigit() and int(request.args.get('page')) > 0:
                page = int(request.args.get('page'))
                movies = movies.offset((page - 1) * page_size)
            return movies.all()
        except Exception as e:
            return {"error": "wrong parameters"}, 404

    def get_one(self, mid):
        return self.session.query(Movies.id, Movies.title, Movies.year,
                                  Movies.description, Movies.trailer,
                                  Movies.genre_id,
                                  Genres.name.label('genre_name'),
                                  Movies.rating,
                                  Movies.director_id
                                  , Directors.name.label('director_name')
                                  ).join(Genres, Movies.genre_id == Genres.id).join(Directors,
                                                                                    Movies.director_id == Directors.id).filter(
            Movies.id == mid
        ).order_by(desc(Movies.year), Movies.title).first()

    def create(self, movie_data):
        mov = Movies(**movie_data)
        self.session.add(mov)
        self.session.commit()
        return mov

    def update(self, mid, movie_details):
        movie_to_edit = Movies.query.get(mid)

        movie_to_edit.title = movie_details.get('title')
        movie_to_edit.description = movie_details.get('description')
        movie_to_edit.trailer = movie_details.get('trailer')
        movie_to_edit.year = movie_details.get('year')
        movie_to_edit.rating = movie_details.get('rating')
        movie_to_edit.genre_id = movie_details.get('genre_id')
        movie_to_edit.director_id = movie_details.get('director_id')

        self.session.add(movie_to_edit)
        self.session.commit()
        return "edited", 201

    def delete(self, mid):
        mov = self.session.query(Movies).get(mid)
        if mov is not None:
            self.session.delete(mov)
            self.session.commit()
            return "deleted", 201
        else:
            return {"err":"no such movie"}, 401
        # return mov
