"""
Script para poblar la base de datos con datos de ejemplo de Star Wars
"""
from app import app
from database.db import db
from models.User import User
from models.Planet import Planet
from models.Character import Character
from models.Favorite import Favorite

def seed_database():
    """Poblar la base de datos con datos de ejemplo"""
    
    with app.app_context():
        # Crear las tablas
        db.create_all()
        
        # Crear usuarios de ejemplo
        user1 = User(email="luke@example.com", password="password123", username="luke_skywalker")
        user2 = User(email="leia@example.com", password="password123", username="princess_leia")
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Crear planetas de ejemplo
        tatooine = Planet(name="Tatooine", climate="arid", terrain="desert")
        alderaan = Planet(name="Alderaan", climate="temperate", terrain="grasslands, mountains")
        hoth = Planet(name="Hoth", climate="frozen", terrain="tundra, ice caves")
        dagobah = Planet(name="Dagobah", climate="murky", terrain="swamp, jungles")
        
        db.session.add(tatooine)
        db.session.add(alderaan)
        db.session.add(hoth)
        db.session.add(dagobah)
        db.session.commit()
        
        # Crear personajes de ejemplo
        luke = Character(name="Luke Skywalker", species="Human", homeworld_id=tatooine.id)
        leia = Character(name="Princess Leia", species="Human", homeworld_id=alderaan.id)
        han = Character(name="Han Solo", species="Human", homeworld_id=None)
        chewbacca = Character(name="Chewbacca", species="Wookiee", homeworld_id=None)
        yoda = Character(name="Yoda", species="Unknown", homeworld_id=dagobah.id)
        
        db.session.add(luke)
        db.session.add(leia)
        db.session.add(han)
        db.session.add(chewbacca)
        db.session.add(yoda)
        db.session.commit()
        
        # Crear algunos favoritos de ejemplo
        favorite1 = Favorite(user_id=user1.id, planet_id=tatooine.id, character_id=None)
        favorite2 = Favorite(user_id=user1.id, planet_id=None, character_id=yoda.id)
        favorite3 = Favorite(user_id=user2.id, planet_id=alderaan.id, character_id=None)
        
        db.session.add(favorite1)
        db.session.add(favorite2)
        db.session.add(favorite3)
        db.session.commit()
        
        print("✅ Base de datos poblada con datos de ejemplo exitosamente!")
        print(f"✅ Usuarios creados: {User.query.count()}")
        print(f"✅ Planetas creados: {Planet.query.count()}")
        print(f"✅ Personajes creados: {Character.query.count()}")
        print(f"✅ Favoritos creados: {Favorite.query.count()}")

if __name__ == "__main__":
    seed_database() 