"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from database.db import db
from models.user import User
from models.character import Character
from models.planet import Planet
from models.favorite import Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ========== ENDPOINTS BÁSICOS ==========

# [GET] /people - Listar todos los personajes
@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        characters = Character.query.all()
        return jsonify([character.serialize() for character in characters]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# [GET] /people/<int:people_id> - Obtener un personaje específico
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    try:
        character = Character.query.get(people_id)
        if character is None:
            return jsonify({"error": "Character not found"}), 404
        return jsonify(character.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# [GET] /planets - Listar todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()
        return jsonify([planet.serialize() for planet in planets]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# [GET] /planets/<int:planet_id> - Obtener un planeta específico
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({"error": "Planet not found"}), 404
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== ENDPOINTS DE USUARIOS ==========

# [GET] /users - Listar todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# [GET] /users/favorites - Obtener favoritos del primer usuario (simulamos usuario actual)
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    try:
        # Por simplicidad, usamos el usuario con ID 1 como "usuario actual"
        user = User.query.first()
        if user is None:
            return jsonify({"error": "No users found"}), 404
        
        favorites = Favorite.query.filter_by(user_id=user.id).all()
        
        # Separamos favoritos por tipo
        favorite_planets = []
        favorite_characters = []
        
        for favorite in favorites:
            if favorite.planet_id:
                planet = Planet.query.get(favorite.planet_id)
                if planet:
                    favorite_planets.append(planet.serialize())
            
            if favorite.character_id:
                character = Character.query.get(favorite.character_id)
                if character:
                    favorite_characters.append(character.serialize())
        
        return jsonify({
            "user": user.serialize(),
            "favorite_planets": favorite_planets,
            "favorite_characters": favorite_characters
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== ENDPOINTS PARA AGREGAR FAVORITOS ==========

# [POST] /favorite/planet/<int:planet_id> - Agregar planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        # Verificar que el planeta existe
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({"error": "Planet not found"}), 404
        
        # Usar el primer usuario como "usuario actual"
        user = User.query.first()
        if user is None:
            return jsonify({"error": "No users found"}), 404
        
        # Verificar que no sea ya favorito
        existing_favorite = Favorite.query.filter_by(
            user_id=user.id, 
            planet_id=planet_id
        ).first()
        
        if existing_favorite:
            return jsonify({"error": "Planet is already a favorite"}), 400
        
        # Crear nuevo favorito
        new_favorite = Favorite(
            user_id=user.id,
            planet_id=planet_id,
            character_id=None
        )
        
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({"message": "Planet added to favorites"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# [POST] /favorite/people/<int:people_id> - Agregar personaje favorito
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        # Verificar que el personaje existe
        character = Character.query.get(people_id)
        if character is None:
            return jsonify({"error": "Character not found"}), 404
        
        # Usar el primer usuario como "usuario actual"
        user = User.query.first()
        if user is None:
            return jsonify({"error": "No users found"}), 404
        
        # Verificar que no sea ya favorito
        existing_favorite = Favorite.query.filter_by(
            user_id=user.id, 
            character_id=people_id
        ).first()
        
        if existing_favorite:
            return jsonify({"error": "Character is already a favorite"}), 400
        
        # Crear nuevo favorito
        new_favorite = Favorite(
            user_id=user.id,
            planet_id=None,
            character_id=people_id
        )
        
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({"message": "Character added to favorites"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ========== ENDPOINTS PARA ELIMINAR FAVORITOS ==========

# [DELETE] /favorite/planet/<int:planet_id> - Eliminar planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        # Usar el primer usuario como "usuario actual"
        user = User.query.first()
        if user is None:
            return jsonify({"error": "No users found"}), 404
        
        # Buscar el favorito
        favorite = Favorite.query.filter_by(
            user_id=user.id, 
            planet_id=planet_id
        ).first()
        
        if favorite is None:
            return jsonify({"error": "Favorite planet not found"}), 404
        
        # Eliminar favorito
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "Planet removed from favorites"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# [DELETE] /favorite/people/<int:people_id> - Eliminar personaje favorito
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    try:
        # Usar el primer usuario como "usuario actual"
        user = User.query.first()
        if user is None:
            return jsonify({"error": "No users found"}), 404
        
        # Buscar el favorito
        favorite = Favorite.query.filter_by(
            user_id=user.id, 
            character_id=people_id
        ).first()
        
        if favorite is None:
            return jsonify({"error": "Favorite character not found"}), 404
        
        # Eliminar favorito
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "Character removed from favorites"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
