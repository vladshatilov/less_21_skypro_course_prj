from dao.genre import GenreDAO


class GenreService:

    def __init__(self, dao: GenreDAO):
        self.this_dao = dao

    def get_all_genres(self):
        return self.this_dao.get_all()

    def get_one_genre(self,mid):
        return self.this_dao.get_one(mid)

    def create_genre(self,genre_details):
        return self.this_dao.create_genre(genre_details)

    def update_genre(self,sid, genre_details):
        return self.this_dao.update_genre(sid, genre_details)

    def delete_genre(self,sid):
        return self.this_dao.delete_genre(sid)