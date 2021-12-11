from sqlalchemy.orm import relationship

from setup_db import db


class Genres(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))

