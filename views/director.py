from flask import jsonify, request
from flask_restx import Namespace, Resource

from dao.model.movies import Usefull_scheme
from implemented import director_service
from service.user import auth_required, admin_required

directors_ns = Namespace('directors')


@directors_ns.route('/')
class Directors_view(Resource):
    # @auth_required
    def get(self):
        all_directors = director_service.get_all_directors()
        return jsonify(Usefull_scheme(many=True).dump(all_directors))

    @admin_required
    def post(self):
        director_details = request.json
        dir = director_service.create_director(director_details)
        return jsonify(Usefull_scheme().dump(dir))

@directors_ns.route('/<int:sid>')
class Director_view(Resource):
    # @auth_required
    def get(self,sid):
        one_director = director_service.get_one_director(sid)
        return jsonify(Usefull_scheme().dump(one_director))


    @admin_required
    def put(self,sid):
        director_details = request.json
        dir = director_service.update_director(sid, director_details)
        return "updated", 201

    @admin_required
    def delete(self,sid):
        mov = director_service.delete_director(sid)
        return "deleted", 204