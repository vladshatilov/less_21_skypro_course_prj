from dao.director import DirectorDAO


class DirectorService:

    def __init__(self, dao: DirectorDAO):
        self.this_dao = dao

    def get_all_directors(self):
        return self.this_dao.get_all()

    def get_one_director(self,mid):
        return self.this_dao.get_one(mid)

    def create_director(self,dir_data):
        return self.this_dao.create_director(dir_data)

    def update_director(self,sid,dir_data):
        return self.this_dao.update_director(sid,dir_data)

    def delete_director(self,sid):
        return self.this_dao.delete_director(sid)
