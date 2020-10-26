# alchemy_app.py
from app import app, db
from app.models import CityModel, TeamModel, PlayerModel, User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'TeamModel': TeamModel, 'CityModel': CityModel, 'PlayerModel': PlayerModel}