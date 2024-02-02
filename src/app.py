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
from models import db, User, Person, Planet, Vehicle, Favourite
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

# GET para mostrar todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_user():
    users_query = User.query.all()
    users_data = list(map(lambda item: item.serialize(), users_query))
    response_body = {
        "msg": "ok",
        "users": users_data
    }

    return jsonify(response_body), 200

# GET para mostrar todos las personas
@app.route('/persons', methods=['GET'])
def get_all_persons():
    persons_query = Person.query.all()
    persons_data = list(map(lambda item: item.serialize(), persons_query))
    response_body = {
        "msg": "ok",
        "persons": persons_data
    }

    return jsonify(response_body), 200

# GET para mostrar un usuario
@app.route('/persons/<int:id>', methods=['GET'])
def person(id):
    person_query = Person.query.filter_by(id = id).first()
    person_data = person_query.serialize()
    response_body = {
        "msg": "ok",
        "person": person_data
    }

    return jsonify(response_body), 200

# GET para mostrar todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planet():
    planet_query = Planet.query.all()
    planet_data = list(map(lambda item: item.serialize(), planet_query))
    response_body = {
        "msg": "ok",
        "planets": planet_data
    }

    return jsonify(response_body), 200

# GET para mostrar un planeta
@app.route('/planets/<int:id>', methods=['GET'])
def planet(id):
    planet_query = Planet.query.filter_by(id = id).first()
    planet_data = planet_query.serialize()
    response_body = {
        "msg": "ok",
        "person": planet_data
    }

    return jsonify(response_body), 200

# GET para mostrar todos los vehiculos
@app.route('/vehicles', methods=['GET'])
def get_all_vehicle():
    vehicle_query = Vehicle.query.all()
    vehicle_data = list(map(lambda item: item.serialize(), vehicle_query))
    response_body = {
        "msg": "ok",
        "vehicles": vehicle_data
    }

    return jsonify(response_body), 200

# GET para mostrar un vehiculo
@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicle(id):
    vehicle_query = Vehicle.query.filter_by(id = id).first()
    vehicle_data = vehicle_query.serialize()
    response_body = {
        "msg": "ok",
        "person": vehicle_data
    }

    return jsonify(response_body), 200

# GET para mostrar todos los favoritos de un usuario
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_favoutites(user_id):
    favourite_query = Favourite.query.filter_by(user_id = user_id).all()
    # print(favourite_query)
    favourite_data = list(map(lambda item: item.serialize(), favourite_query))
    # print(favourite_data)
    response_body = {
        "msg": "ok",
        "favourite " + str(user_id): favourite_data
    }

    return jsonify(response_body), 200

# POST Crear nueva persona favorita
@app.route('/users/<int:user_id>/favorites/person/<int:person_id>', methods=['POST'])
def Create_one_people_favoutite(user_id, person_id):
    new_person_favourite = Favourite(user_id = user_id, person_id = person_id)
    db.session.add(new_person_favourite)
    db.session.commit()
    return jsonify("Personaje favorito añadido"), 200

# POST Crear nuevo planeta favorito
@app.route('/users/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def Create_one_planet_favoutite(user_id, planet_id):
    new_planet_favourite = Favourite(user_id = user_id, planet_id = planet_id)
    db.session.add(new_planet_favourite)
    db.session.commit()
    return jsonify("Planeta favorito añadido"), 200

# POST Crear nuevo vehiculo favorito
@app.route('/users/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['POST'])
def Create_one_vehicle_favoutite(user_id, vehicle_id):
    new_vehicle_favourite = Favourite(user_id = user_id, vehicle_id = vehicle_id)
    db.session.add(new_vehicle_favourite)
    db.session.commit()
    return jsonify("Vehiculo favorito añadido"), 200

# DELETE Eliminar persona favorita
@app.route('/users/<int:user_id>/favorites/person/<int:person_id>', methods=['DELETE'])
def Delete_one_people_favoutite(user_id, person_id):
    delete_person_favourite = Favourite.query.filter_by(user_id=user_id, person_id=person_id ).first()
    db.session.delete(delete_person_favourite)
    db.session.commit()
    return jsonify("Personaje favorito eliminado"), 200

# DELETE Eliminar planeta favorito
@app.route('/users/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def Delete_one_planet_favoutite(user_id, planet_id):
    delete_planet_favourite = Favourite.query.filter_by(user_id=user_id, planet_id=planet_id ).first()
    db.session.delete(delete_planet_favourite)
    db.session.commit()
    return jsonify("Planeta favorito eliminado"), 200

# DELETE Eliminar vehiculo favorito
@app.route('/users/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['DELETE'])
def Delete_one_vehicle_favoutite(user_id, vehicle_id):
    delete_vehicle_favourite = Favourite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id ).first()
    db.session.delete(delete_vehicle_favourite)
    db.session.commit()
    return jsonify("Vehiculo favorito eliminado"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
