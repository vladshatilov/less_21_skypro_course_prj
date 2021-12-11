from dao.model.movies import Movies
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one_by_name(self, username):
        user = self.session.query(User).filter(User.name == username).first()
        return user

    def get_one_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        return user

    def get_one_by_email_about(self, email):
        user = self.session.query(User.email, User.id, User.name,User.surname, User.favourite_genre).filter(User.email == email).first()
        return user

    def get_user_favourites(self,email):
        user = self.get_one_by_email(email)
        if user is None:
            return {"error": "Wrong authentication data"}, 401

        return list(user.movie)

    def get_all(self):
        return self.session.query(User.email, User.id, User.name,User.surname, User.role).all()

    def patch_user_about(self, email,json_obj):
        user = self.get_one_by_email(email)
        name = json_obj.get('name', None)
        surname = json_obj.get('surname', None)
        try:
            favourite_genre = int(json_obj.get('favourite_genre', None))
        except Exception as e:
            return {"error": "incorrect genre id"}, 404
        if name is not None:
            user.name = name
        if surname is not None:
            user.surname = surname
        if favourite_genre is not None:
            user.favourite_genre = favourite_genre
        self.session.add(user)
        self.session.commit()
        # return user
        return {"success": "success"}, 201

    def put_user_password(self,user,new_password):
        user.password = new_password
        self.session.add(user)
        self.session.commit()
        return user

    def get_tokens(self, json_obj):
        pass

    def create_user(self,json_obj):
        u1 = User(**json_obj)
        # with self.session.begin():
        self.session.add(u1)
        self.session.commit()

    def add_movie_to_liked(self,email,uid):
        user = self.get_one_by_email(email)
        if user is None:
            return {"error": "Wrong authentication data"}, 401

        c1 = Movies.query.get(uid)
        if c1 is None:
            return {"error": "Wrong movie id"}, 401
        user.movie.append(c1)
        self.session.add(user)
        self.session.commit()
        return {"info": "added to like list"}, 201

    def remove_movie_from_liked(self,email,uid):
        user = self.get_one_by_email(email)
        if user is None:
            return {"error": "Wrong authentication data"}, 401

        user.movie = list(filter(lambda a: a.id != uid, user.movie))
        self.session.commit()
        return {"info": "removed from like list"}, 201