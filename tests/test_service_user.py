import pytest
from unittest.mock import MagicMock

from flask import jsonify


from dao.model.director import Directors
from dao.model.genre import Genres
from dao.model.movies import Movies
from dao.model.user import User
from dao.user import UserDAO
from service.user import UserService


@pytest.fixture()
def user_dao():
    user_dao = UserDAO(None)
    u1 = User(id=1,
               name="test",
               surname="ee",
               email="t@mail.ru",
               password="00000000")
    u2 = User(id=2,
               name="test2",
               surname="ee2",
               email="t2@mail.ru",
               password="00000029")

    m1 = Movies(title="Омерзительная восьмерка",
               id=1,
               year=2015,
               trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
               description="США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество= генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
               rating=7.8)
    m2 = Movies(title="Дюна",
               id=2,
               year=2015,
               trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
               description="Это история любви старлетки, которая между прослушиваниями подает кофе состоявшимся кинозвездам, и фанатичного джазового музыканта, вынужденного подрабатывать в заштатных барах. Но пришедший к влюбленным успех начинает подтачивать их отношения.",
               rating=8.8)

    user_dao.get_one_by_email = MagicMock(return_value=u1)
    user_dao.get_one_by_email_about = MagicMock(return_value=u1)
    user_dao.get_user_favourites = MagicMock(return_value=[m1,m2])
    user_dao.get_all = MagicMock(return_value=[u1, u2])
    user_dao.patch_user_about = MagicMock(return_value=u1)
    user_dao.put_user_password = MagicMock()
    user_dao.add_movie_to_liked = MagicMock()
    user_dao.remove_movie_from_liked = MagicMock()
    user_dao.create_user = MagicMock(return_value=User(id=1))
    return user_dao


class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self,user_dao):
        self.user_service = UserService(user_dao)

    def test_get_one(self):
        user_one = self.user_service.get_one_by_email("t@mail.ru")
        assert user_one is not None
        assert user_one.name == "test"
        assert user_one.surname == 'ee'

    def test_bad_get_one(self, user_dao):
        user_dao.get_one_by_email.return_value = None
        user_one = self.user_service.get_one_by_email(None)
        assert user_one is None

    def test_get_all(self):
        users = self.user_service.get_all()
        assert len(users) == 2

    def test_create(self):
        user_one = {
            "id": 7,
            "name": "test",
            "email": "y@mail.ua",
            "password": "7.2"
        }
        user = self.user_service.create_new_user(user_one)
        assert user_one['id'] is not None
        assert user_one['name'] == "test"



