from dao.model.director import Directors


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Directors).all()

    def get_one(self, did):
        return self.session.query(Directors).get(did)

    def create_director(self,dir_data):
        dir = Directors(**dir_data)
        self.session.add(dir)
        self.session.commit()
        return dir

    def update_director(self,sid, dir_data):
        item_to_edit = Directors.query.get(sid)
        item_to_edit.id = dir_data.get('id')
        item_to_edit.name = dir_data.get('name')

        self.session.add(item_to_edit)
        self.session.commit()
        return "edited", 201

    def delete_director(self,sid):
        item = self.session.query(Directors).get(sid)
        self.session.delete(item)
        self.session.commit()
        return item