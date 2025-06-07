# Routes package
from .users import users_bp
from .characters import characters_bp  
from .planets import planets_bp
from .favorites import favorites_bp

__all__ = ['users_bp', 'characters_bp', 'planets_bp', 'favorites_bp'] 