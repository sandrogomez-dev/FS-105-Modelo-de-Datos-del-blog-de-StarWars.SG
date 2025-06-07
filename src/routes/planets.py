from flask import Blueprint, jsonify
from models.Planet import Planet
from models.Character import Character

planets_bp = Blueprint('planets', __name__)

@planets_bp.route('/planets', methods=['GET'])
def get_planets():
    """Listar todos los registros de planets en la base de datos"""
    try:
        planets = Planet.query.all()
        planets_list = []
        
        for planet in planets:
            # Obtener los personajes que son de este planeta
            residents = Character.query.filter_by(homeworld_id=planet.id).all()
            residents_list = []
            
            for resident in residents:
                residents_list.append({
                    'id': resident.id,
                    'name': resident.name,
                    'species': resident.species
                })
            
            planets_list.append({
                'id': planet.id,
                'name': planet.name,
                'climate': planet.climate,
                'terrain': planet.terrain,
                'residents': residents_list
            })
        
        return jsonify(planets_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@planets_bp.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    """Muestra la información de un solo planeta según su id"""
    try:
        planet = Planet.query.get(planet_id)
        
        if not planet:
            return jsonify({'error': 'Planet not found'}), 404
        
        # Obtener los personajes que son de este planeta
        residents = Character.query.filter_by(homeworld_id=planet.id).all()
        residents_list = []
        
        for resident in residents:
            residents_list.append({
                'id': resident.id,
                'name': resident.name,
                'species': resident.species
            })
        
        planet_data = {
            'id': planet.id,
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'residents': residents_list
        }
        
        return jsonify(planet_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 