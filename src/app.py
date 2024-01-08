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
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/user', methods=['GET'])
def get_users():
    results =[]
    users = User.query.all()
    for user in users:
         results.append(user.serialize())
    return jsonify(results), 200

@app.route('/user', methods=['GET'])
def get_person(person_id):
    person = People.query.get ( person_id)

    if person:
        return jsonify(person.serialize()), 200
    
    return jsonify({'message': 'Person not found'}), 404



#---fAVS
def get_all_favorites (user_id):
    User = User.query.get ( user_id)

    serialize_favorites = []
    for favorite in User.favorites:
        serialize_favorites.append(favorite.serialize())

    if len (serialize_favorites) > 0:
        return jsonify (serialize_favorites), 200
    
    return jsonify({'message': 'Cannot find favorite'}), 404


#---ADD PLANETS
@app.route('/planets', methods=['POST'])
def add_planet():
    req_body = request.get_json()
    person_name = req_body ['name']
    person_mass = req_body ['mass']
    person_environment = req_body ['environment']

    new_planet = People (name = person_name, mass = person_mass, environment = person_environment)

    db.session.add(new_planet)
    db.session.commit()

    return jsonify ({'Message': 'Posted new planet to database'}), 200

#---GET PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    
    planets = Planets.query.all ()
    serialized_planets = []
    for planet in planets:
        serialized_planets.append(planet.serialize())

    if len(serialized_planets) > 0:
        return jsonify(serialized_planets), 200
    
    return jsonify ({'Message': 'No planets in database'}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

# gets a certain planet ID info
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get ( planet_id)

    if planet:
        return jsonify(planet.serialize()), 200
    
    return jsonify({'message': 'Planet not found'}), 404



# add a new favorite planet to the current user 
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet (planet_id):
    user_id = 1

    current_user = User.query.get(user_id)

    if current_user: 
        planet = Planet.query.get(planet_id)

        favorites = Favorites ()
        favorites.user = current_user
        favorites.plamet = planet

        current_user.favorites.append(favorites)
        db.session.commit()

        return jsonify({ 'Message': 'Added planet to user favorites'}), 200
    
    return jsonify({"Message": "Error while Adding planet"}), 404