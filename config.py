class Config(object):
    DEBUG = True
    SECRET_HERE = '249y822324r9v8238r9u'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///Q:/react_apps/flask/flaskProject_lesson21_course_work/movies.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://movieadmin:movie12@127.0.0.1/movie_app'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@172.18.0.2/db1'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@postgres/db1'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    # SQLALCHEMY_ECHO = True
    CORS_HEADERS = 'Content-Type'
