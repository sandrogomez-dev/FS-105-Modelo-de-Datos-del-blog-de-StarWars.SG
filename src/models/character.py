from src.database.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    species = db.Column(db.String(50))
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
