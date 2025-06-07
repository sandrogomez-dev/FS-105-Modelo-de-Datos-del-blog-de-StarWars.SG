from flask import Blueprint, jsonify
from models.Character import Character
from models.Planet import Planet

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/people', methods=['GET'])
def get_people():
    """Listar todos los registros de people en la base de datos"""
    try:
        characters = Character.query.all()
        characters_list = []
        
        for character in characters:
            homeworld = None
            if character.homeworld_id:
                planet = Planet.query.get(character.homeworld_id)
                if planet:
                    homeworld = {
                        'id': planet.id,
                        'name': planet.name,
                        'climate': planet.climate,
                        'terrain': planet.terrain
                    }
            
            characters_list.append({
                'id': character.id,
                'name': character.name,
                'species': character.species,
                'homeworld_id': character.homeworld_id,
                'homeworld': homeworld
            })
        
        return jsonify(characters_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@characters_bp.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    """Muestra la información de un solo personaje según su id"""
    try:
        character = Character.query.get(people_id)
        
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        
        homeworld = None
        if character.homeworld_id:
            planet = Planet.query.get(character.homeworld_id)
            if planet:
                homeworld = {
                    'id': planet.id,
                    'name': planet.name,
                    'climate': planet.climate,
                    'terrain': planet.terrain
                }
        
        character_data = {
            'id': character.id,
            'name': character.name,
            'species': character.species,
            'homeworld_id': character.homeworld_id,
            'homeworld': homeworld
        }
        
        return jsonify(character_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 