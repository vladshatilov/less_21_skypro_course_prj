from flask import jsonify, request, abort
from flask_restx import Namespace, Resource

from dao.model.movies import Usefull_scheme
from implemented import user_service
from service.user import auth_required

user_ns = Namespace('/')


@user_ns.route('/user')
class User_List(Resource):
    @auth_required
    def get(self):
        # request_json = request.json
        user = user_service.get_user_about()
        return jsonify(Usefull_scheme().dump(user))

    @auth_required
    def patch(self):
        request_json = request.json
        user = user_service.patch_user_about(request_json)

        # response = jsonify(user) #jsonify(Usefull_scheme(many=True).dump(all_movies))
        # ### test for CORS
        # response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add('Access-Control-Allow-Headers', "*")
        # response.headers.add('Access-Control-Allow-Methods', "DELETE,PATCH, POST, GET, OPTIONS")
        # # return jsonify(Usefull_scheme(many=True).dump(all_movies))
        # return response

        # return jsonify(Usefull_scheme().dump(user))
        return jsonify(user)


@user_ns.route('/user/password')
class User_Pass_Update(Resource):
    def put(self):
        request_json = request.json
        print(request_json)
        user = user_service.update_user_password(request_json)
        return jsonify(Usefull_scheme().dump(user))


@user_ns.route('/favorites/movies/')
class User_GetFavourites(Resource):
    @auth_required
    def get(self):
        response = user_service.get_user_favourites()
        print(response)
        return jsonify(Usefull_scheme(many=True).dump(response))

@user_ns.route('/favorites/movies/<int:uid>')
class User_Favourites(Resource):
    @auth_required
    def post(self,uid):
        response = user_service.add_movie_to_liked(uid)
        return jsonify(response)

    @auth_required
    def delete(self,uid):
        response = user_service.removie_movie_from_liked(uid)
        return jsonify(response)


@user_ns.route('/auth/login')
class User_Login(Resource):
    def post(self):
        request_json = request.json
        tokens = user_service.get_access_token(request_json)
        return jsonify(tokens)

    def put(self):
        request_json = request.json
        tokens = user_service.update_access_token(request_json)
        return jsonify(tokens)


@user_ns.route('/auth/register')
class User_Register(Resource):
    def post(self):
        request_json = request.json
        if request_json is None:
            abort(401)
        tokens = user_service.create_new_user(request_json)
        return jsonify(tokens)
