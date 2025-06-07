from flask import Blueprint, jsonify, request
from models.User import User
from models.Favorite import Favorite
from models.Planet import Planet
from models.Character import Character
from database.db import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    """Listar todos los usuarios del blog"""
    try:
        users = User.query.all()
        users_list = []
        
        for user in users:
            users_list.append({
                'id': user.id,
                'email': user.email,
                'username': user.username
            })
        
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    """Listar todos los favoritos que pertenecen al usuario actual"""
    # Por ahora usaremos el usuario con ID 1 como usuario actual
    # En un sistema real, esto vendría del token de autenticación
    user_id = request.args.get('user_id', 1, type=int)
    
    try:
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        favorites_list = []
        
        for favorite in favorites:
            favorite_data = {
                'id': favorite.id,
                'user_id': favorite.user_id
            }
            
            # Si es un planeta favorito
            if favorite.planet_id:
                planet = Planet.query.get(favorite.planet_id)
                if planet:
                    favorite_data['type'] = 'planet'
                    favorite_data['planet'] = {
                        'id': planet.id,
                        'name': planet.name,
                        'climate': planet.climate,
                        'terrain': planet.terrain
                    }
            
            # Si es un personaje favorito
            if favorite.character_id:
                character = Character.query.get(favorite.character_id)
                if character:
                    favorite_data['type'] = 'character'
                    favorite_data['character'] = {
                        'id': character.id,
                        'name': character.name,
                        'species': character.species,
                        'homeworld_id': character.homeworld_id
                    }
            
            favorites_list.append(favorite_data)
        
        return jsonify(favorites_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 