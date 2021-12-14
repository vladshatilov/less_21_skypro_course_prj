from unittest.mock import MagicMock

import pytest as pytest

from dao.director import DirectorDAO
from dao.model.director import Directors
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    dir_dao = DirectorDAO(None)
    d1 = Directors(id=1, name='Dddao')
    d2 = Directors(id=2, name='MsX')
    d3 = Directors(id=3, name='MrD')

    dir_dao.get_one = MagicMock(return_value=d1)
    dir_dao.get_all = MagicMock(return_value=[d1, d2, d3])
    dir_dao.create_director = MagicMock(return_value=Directors(id=1))
    dir_dao.delete_director = MagicMock()
    dir_dao.update_director = MagicMock()
    return dir_dao

def test_one():
    assert 1==1

class TestDirectorService():
    @pytest.fixture(autouse=True)
    def dir_service(self, director_dao):
        self.dir_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        dir_one = self.dir_service.get_one_director(1)
        assert dir_one is not None
        assert dir_one.id == 1
        assert dir_one.name == 'Dddao'

    def test_bad_get_one(self,director_dao):
        director_dao.get_one.return_value=None
        dir_one = self.dir_service.get_one_director(None)
        assert dir_one is None

    def test_get_all(self):
        dirs = self.dir_service.get_all_directors()
        assert len(dirs)>0

    def test_create(self):
        dir_d ={"id":1,"name":"ss"}
        user = self.dir_service.create_director(dir_d)
        assert dir_d['id'] is not None

    def test_update(self):
        dir_d = {"id": 1, "name": "ss"}
        self.dir_service.update_director(1,dir_d)

    def test_partially_update(self):
        dir_d = {"id": 1, "name": "ss"}
        self.dir_service.update_director(1,dir_d)

    def test_bad_partially_update(self):
        dir_d = {"id": 41}
        self.dir_service.update_director(1,dir_d)

    def test_delete(self):
        self.dir_service.delete_director(1)

    def test_bad_delete(self):
        self.dir_service.delete_director(None)
