from database.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    species = db.Column(db.String(50))
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "homeworld_id": self.homeworld_id
        }
