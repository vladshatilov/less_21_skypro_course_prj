import calendar
import datetime
import hashlib

import jwt
from flask import request
from flask_restx import abort

from constants import PWD_HASH_ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_ALGO
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one_by_name(self, username):
        return self.dao.get_one_by_name(username)

    def get_one_by_email(self, email):
        return self.dao.get_one_by_email(email)

    def get_all(self):
        return self.dao.get_all()

    def get_user_about(self):
        token_with_data = request.headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token_with_data, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        email = data.get("email")
        return self.dao.get_one_by_email_about(email)

    def get_user_favourites(self):
        token_with_data = request.headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token_with_data, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        email = data.get("email")
        return self.dao.get_user_favourites(email)

    def patch_user_about(self,json_obj):
        token_with_data = request.headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token_with_data, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        email = data.get("email")

        return self.dao.patch_user_about(email,json_obj)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(PWD_HASH_ALGO, password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS)

    def create_new_user(self, json_obj):
        # name = json_obj.get('name', None)
        email = json_obj.get('email', None)
        password = json_obj.get('password', None)
        surname = json_obj.get('surname', None)
        if None in [email, password]:
            abort(401)

        user = self.get_one_by_email(email)
        if user is not None:
            return {"error": "User already exists"}, 401
        self.dao.create_user({
            "name": json_obj.get("name"),
            "email": json_obj.get("email"),
            "password": self.get_hash(json_obj.get("password")),
            "surname": json_obj.get("surname"),
            "role": "user"
        })

        data = {
            "email": email,
            "role": "user"
        }
        secret = PWD_HASH_SALT
        algo = JWT_ALGO
        expired_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(expired_date.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days180 = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data['exp'] = calendar.timegm(days180.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201

    def get_access_token(self, json_obj):
        # name = json_obj.get('name', None)
        email = json_obj.get('email', None)
        password = json_obj.get('password', None)
        if None in [email, password]:
            abort(401)

        user = self.get_one_by_email(email)
        if user is None:
            return {"error": "Wrong authentication data"}, 401

        password_hash = self.get_hash(password)
        if password_hash != user.password:
            return {"error": "Wrong authentication data"}, 401

        data = {
            "email": user.email,
            "role": user.role
        }
        secret = PWD_HASH_SALT
        algo = JWT_ALGO
        expired_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(expired_date.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days180 = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data['exp'] = calendar.timegm(days180.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        # print(tokens)
        return tokens

    def update_access_token(self, json_obj):
        refresh_token = json_obj.get('refresh_token')
        if refresh_token is None:
            abort(400)

        secret = PWD_HASH_SALT
        algo = JWT_ALGO
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        email = data.get("email")
        user = self.get_one_by_email(email)

        data = {
            "email": user.email,
            "role": user.role
        }
        expired_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(expired_date.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days180 = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data['exp'] = calendar.timegm(days180.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    def update_user_password(self, json_obj):
        password = json_obj.get('password', None)
        new_password = json_obj.get('new_password', None)

        if None in [password,new_password]:
            abort(401)

        token_with_data = request.headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token_with_data, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        email = data.get("email")

        user = self.get_one_by_email(email)
        password_hash = self.get_hash(password)

        if password_hash != user.password:
            return {"error": "Wrong authentication data"}, 401

        return self.dao.put_user_password(user,self.get_hash(new_password))

    def add_movie_to_liked(self,uid):
        token_with_data = request.headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token_with_data, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        email = data.get("email")

        if None in [email, uid]:
            abort(401)

        return self.dao.add_movie_to_liked(email,uid)

    def removie_movie_from_liked(self,uid):
        token_with_data = request.headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token_with_data, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        email = data.get("email")

        if None in [email, uid]:
            abort(401)

        return self.dao.remove_movie_from_liked(email, uid)





def auth_required(func):
    def wrapper(*args, **kwargs):
        if not "Authorization" in request.headers:
            abort(401)
        try:
            token_to_check = request.headers['Authorization'].split('Bearer ')[-1]
            res = jwt.decode(token_to_check, PWD_HASH_SALT, algorithms=[JWT_ALGO])
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        try:
            token_to_check = request.headers['Authorization'].split('Bearer ')[-1]
            user = jwt.decode(token_to_check, PWD_HASH_SALT, algorithms=[JWT_ALGO])
            role = user.get('role')
            if role != 'admin':
                abort(401)
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)

        return func(*args, **kwargs)

    return wrapper
