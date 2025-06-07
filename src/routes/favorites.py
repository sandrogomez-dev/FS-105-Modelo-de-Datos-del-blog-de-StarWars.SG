from flask import Blueprint, jsonify, request
from models.Favorite import Favorite
from models.Planet import Planet
from models.Character import Character
from models.User import User
from database.db import db

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    """Añade un nuevo planet favorito al usuario actual con el id = planet_id"""

    user_id = request.json.get('user_id', 1) if request.json else 1
    
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'error': 'Planet not found'}), 404
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        existing_favorite = Favorite.query.filter_by(
            user_id=user_id, 
            planet_id=planet_id
        ).first()
        
        if existing_favorite:
            return jsonify({'error': 'Planet already in favorites'}), 400
        
        new_favorite = Favorite(
            user_id=user_id,
            planet_id=planet_id,
            character_id=None
        )
        
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Planet added to favorites successfully',
            'favorite': {
                'id': new_favorite.id,
                'user_id': new_favorite.user_id,
                'planet_id': new_favorite.planet_id,
                'planet_name': planet.name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorites_bp.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    """Añade un nuevo people favorito al usuario actual con el id = people_id"""
    user_id = request.json.get('user_id', 1) if request.json else 1
    
    try:
        character = Character.query.get(people_id)
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        existing_favorite = Favorite.query.filter_by(
            user_id=user_id, 
            character_id=people_id
        ).first()
        
        if existing_favorite:
            return jsonify({'error': 'Character already in favorites'}), 400
        
        new_favorite = Favorite(
            user_id=user_id,
            planet_id=None,
            character_id=people_id
        )
        
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Character added to favorites successfully',
            'favorite': {
                'id': new_favorite.id,
                'user_id': new_favorite.user_id,
                'character_id': new_favorite.character_id,
                'character_name': character.name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorites_bp.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    """Elimina un planet favorito con el id = planet_id"""
    user_id = request.args.get('user_id', 1, type=int)
    
    try:
        favorite = Favorite.query.filter_by(
            user_id=user_id, 
            planet_id=planet_id
        ).first()
        
        if not favorite:
            return jsonify({'error': 'Favorite planet not found'}), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Planet removed from favorites successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorites_bp.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    """Elimina un people favorito con el id = people_id"""
    user_id = request.args.get('user_id', 1, type=int)
    
    try:
        favorite = Favorite.query.filter_by(
            user_id=user_id, 
            character_id=people_id
        ).first()
        
        if not favorite:
            return jsonify({'error': 'Favorite character not found'}), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Character removed from favorites successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 