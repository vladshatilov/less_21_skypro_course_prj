from dao.model.genre import Genres


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Genres).all()

    def get_one(self, gid):
        return self.session.query(Genres).get(gid)

    def create_genre(self,genre_data):
        item = Genres(**genre_data)
        self.session.add(item)
        self.session.commit()
        return item

    def update_genre(self,sid, dir_data):
        item_to_edit = Genres.query.get(sid)
        item_to_edit.id = dir_data.get('id')
        item_to_edit.name = dir_data.get('name')

        self.session.add(item_to_edit)
        self.session.commit()
        return "edited", 201

    def delete_genre(self,sid):
        item = self.session.query(Genres).get(sid)
        self.session.delete(item)
        self.session.commit()
        return item