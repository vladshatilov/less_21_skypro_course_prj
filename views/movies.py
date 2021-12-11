from flask import jsonify, request
from flask_restx import Namespace, Resource

from dao.model.movies import Usefull_scheme
from implemented import movie_service
from service.user import auth_required, admin_required

movies_ns = Namespace('movies')

# @cross_origin()
@movies_ns.route('/')
class Movies_view(Resource):
    # @auth_required
    def get(self):
        all_movies = movie_service.get_all_movies()
        response = jsonify(Usefull_scheme(many=True).dump(all_movies))
        ### test for CORS
        # response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add('Access-Control-Allow-Headers', "*")
        # response.headers.add('Access-Control-Allow-Methods', "*")
        # return jsonify(Usefull_scheme(many=True).dump(all_movies))
        return response

    # @admin_required
    def post(self):
        movie_details = request.json
        mov = movie_service.create_movie(movie_details)
        return jsonify(Usefull_scheme().dump(mov))

@movies_ns.route('/<int:mid>')
class Movie_view(Resource):
    # @auth_required
    def get(self,mid):
        one_movie = movie_service.get_one_movie(mid)
        return jsonify(Usefull_scheme().dump(one_movie))

    @admin_required
    def put(self,mid):
        movie_details = request.json
        mov = movie_service.update_movie(mid, movie_details)
        return "updated", 201

    @admin_required
    def delete(self,mid):
        mov = movie_service.delete_movie(mid)
        return "deleted", 204