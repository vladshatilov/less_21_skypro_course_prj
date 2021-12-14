import pytest
from unittest.mock import MagicMock, patch

from flask import jsonify

from dao.model.director import Directors
from dao.model.genre import Genres
from dao.model.movies import Movies
from dao.model.user import User
from dao.movies import MovieDAO
from dao.user import UserDAO
from service.movies import MovieService
from service.user import UserService


class TestMoviesService:
    @pytest.fixture
    def mov_1(self):
        return Movies(title="Омерзительная восьмерка",
                      id=1,
                      year=2015,
                      trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
                      description="США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество= генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
                      rating=7.8)

    @pytest.fixture
    def mov_2(self):
        return Movies(title="Дюна",
                      id=2,
                      year=2015,
                      trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
                      description="Это история любви старлетки, которая между прослушиваниями подает кофе состоявшимся кинозвездам, и фанатичного джазового музыканта, вынужденного подрабатывать в заштатных барах. Но пришедший к влюбленным успех начинает подтачивать их отношения.",
                      rating=8.8)

    @pytest.fixture
    def mov_dao(self, mov_1, mov_2):
        # m1 = Movies(title="Омерзительная восьмерка",
        #             id=1,
        #             year=2015,
        #             trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
        #             description="США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество= генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
        #             rating=7.8)
        # m2 = Movies(title="Дюна",
        #             id=2,
        #             year=2015,
        #             trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
        #             description="Это история любви старлетки, которая между прослушиваниями подает кофе состоявшимся кинозвездам, и фанатичного джазового музыканта, вынужденного подрабатывать в заштатных барах. Но пришедший к влюбленным успех начинает подтачивать их отношения.",
        #             rating=8.8)

        # with patch('dao.movies.MovieDAO') as mock:
        #     mock = MagicMock(
        #         get_one_movie=MagicMock(return_value=m1),
        #         get_all_movies=MagicMock(),
        #         create_movie=MagicMock(),
        #         delete_movie=MagicMock(),
        #         update_movie=MagicMock(),
        #     )
        #     return mock
        dao = MovieDAO(None)

        dao.get_one = MagicMock(return_value=mov_1)
        dao.get_all = MagicMock(return_value=[mov_1, mov_2])
        dao.update = MagicMock(return_value=mov_1)
        dao.create = MagicMock(return_value=Movies(id=1))
        dao.delete = MagicMock()
        return dao

    @pytest.fixture(autouse=True)
    def movies_service(self, mov_dao):
        self.movie_service = MovieService(mov_dao)

    def test_get_one(self,mov_1):
        # assert mov_1 == self.movie_service.get_one_movie(1)
        movie_one = self.movie_service.get_one_movie(1)
        assert movie_one is not None
        assert movie_one.year == 2015
        assert movie_one.title == 'Омерзительная восьмерка'

    def test_bad_get_one(self,mov_dao):
        mov_dao.get_one.return_value=None
        movie_one = self.movie_service.get_one_movie(None)
        assert movie_one is None

    def test_get_all(self):
        movies = self.movie_service.get_all_movies()
        assert len(movies) == 2

    def test_create(self):
        movie_one = {
            "title": "Чикаго",
            "id": 7,
            "year": 2002,
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "rating": 7.2
        }
        user = self.movie_service.create_movie(movie_one)
        assert movie_one['id'] is not None
        assert movie_one['rating'] == 7.2

    def test_update(self):
        movie_one = {
            "title": "Чикаго",
            "id": 1,
            "year": 2002,
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "rating": 7.2
        }
        self.movie_service.update_movie(1, movie_one)

    def test_partially_update(self):
        movie_one = {
            "title": "Чикаго",
            "id": 1,
            "year": 2002,
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "rating": 7.2
        }
        self.movie_service.update_movie(1,movie_one)

    def test_delete(self):
        self.movie_service.delete_movie(1)

    def test_bad_delete_request(self):
        self.movie_service.delete_movie(None)
