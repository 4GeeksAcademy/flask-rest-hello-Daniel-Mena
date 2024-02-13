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
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# POST Crear Usuario
@app.route('/signup', methods=['POST'])
def signup():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_query = User.query.filter_by(email = email).first()
    if user_query != None:
        return jsonify({"msg": "There is a user with that email"}), 401

    new_user = User(name = name, email = email, password = password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify("Usuario añadido"), 200

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
        "result": persons_data
    }

    return jsonify(response_body), 200

# GET para mostrar un personaje
@app.route('/persons/<int:id>', methods=['GET'])
def person(id):
    person_query = Person.query.filter_by(id = id).first()
    person_data = person_query.serialize()
    response_body = {
        "msg": "ok",
        "result": person_data
    }

    return jsonify(response_body), 200

# GET para mostrar todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planet():
    planet_query = Planet.query.all()
    planet_data = list(map(lambda item: item.serialize(), planet_query))
    response_body = {
        "msg": "ok",
        "result": planet_data
    }

    return jsonify(response_body), 200

# GET para mostrar un planeta
@app.route('/planets/<int:id>', methods=['GET'])
def planet(id):
    planet_query = Planet.query.filter_by(id = id).first()
    planet_data = planet_query.serialize()
    response_body = {
        "msg": "ok",
        "result": planet_data
    }

    return jsonify(response_body), 200

# GET para mostrar todos los vehiculos
@app.route('/vehicles', methods=['GET'])
def get_all_vehicle():
    vehicle_query = Vehicle.query.all()
    vehicle_data = list(map(lambda item: item.serialize(), vehicle_query))
    response_body = {
        "msg": "ok",
        "result": vehicle_data
    }

    return jsonify(response_body), 200

# GET para mostrar un vehiculo
@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicle(id):
    vehicle_query = Vehicle.query.filter_by(id = id).first()
    vehicle_data = vehicle_query.serialize()
    response_body = {
        "msg": "ok",
        "result": vehicle_data
    }

    return jsonify(response_body), 200

# POST Para hacer login
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_query = User.query.filter_by(email = email).first()
    if user_query is None:
        return jsonify({"msg": "Correo no existe"}), 401
    if email != user_query.email or password != user_query.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
# GET para mostrar todos los favoritos de un usuario
@app.route("/user/favorites", methods=["GET"])
@jwt_required()
def get_all_favourites():
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    favourite_query = Favourite.query.filter_by(user_id = user_query.id).all()
    favourite_data = list(map(lambda item: item.serialize(), favourite_query))
    response_body = {
        "msg": "ok",
        "favourite": favourite_data
    }

    return jsonify(response_body), 200

# POST Crear nueva persona favorita
@app.route('/user/favorites/persons/<int:person_id>', methods=['POST'])
@jwt_required()
def Create_one_people_favoutite(person_id):
    url = request.json.get("url", None)
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    new_person_favourite = Favourite(user_id = user_query.id, url = url, person_id = person_id)
    db.session.add(new_person_favourite)
    db.session.commit()
    return jsonify("Personaje favorito añadido"), 200

# POST Crear nuevo planeta favorito
@app.route('/user/favorites/planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def Create_one_planet_favoutite(planet_id):
    url = request.json.get("url", None)
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    new_planet_favourite = Favourite(user_id = user_query.id, url = url, planet_id = planet_id)
    db.session.add(new_planet_favourite)
    db.session.commit()
    return jsonify("Planeta favorito añadido"), 200

# POST Crear nuevo vehiculo favorito
@app.route('/user/favorites/vehicles/<int:vehicle_id>', methods=['POST'])
@jwt_required()
def Create_one_vehicle_favoutite(vehicle_id):
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    new_vehicle_favourite = Favourite(user_id = user_query.id, vehicle_id = vehicle_id)
    db.session.add(new_vehicle_favourite)
    db.session.commit()
    return jsonify("Vehiculo favorito añadido"), 200

# DELETE Eliminar favorito
@app.route('/user/favorites/<int:id>', methods=['DELETE'])
@jwt_required()
def Delete_one_favoutite(id):
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    delete_person_favourite = Favourite.query.filter_by(user_id=user_query.id, id=id).first()
    db.session.delete(delete_person_favourite)
    db.session.commit()
    return jsonify("Elemento favorito eliminado"), 200

# DELETE Eliminar persona favorita
@app.route('/user/favorites/persons/<int:person_id>', methods=['DELETE'])
@jwt_required()
def Delete_one_people_favoutite(person_id):
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    delete_person_favourite = Favourite.query.filter_by(user_id=user_query.id, person_id=person_id ).first()
    db.session.delete(delete_person_favourite)
    db.session.commit()
    return jsonify("Personaje favorito eliminado"), 200

# DELETE Eliminar planeta favorito
@app.route('/user/favorites/planets/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def Delete_one_planet_favoutite(planet_id):
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    delete_planet_favourite = Favourite.query.filter_by(user_id=user_query.id, planet_id=planet_id ).first()
    db.session.delete(delete_planet_favourite)
    db.session.commit()
    return jsonify("Planeta favorito eliminado"), 200

# DELETE Eliminar vehiculo favorito
@app.route('/user/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def Delete_one_vehicle_favoutite(vehicle_id):
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email = current_user).first()
    delete_vehicle_favourite = Favourite.query.filter_by(user_id=user_query.id, vehicle_id=vehicle_id ).first()
    db.session.delete(delete_vehicle_favourite)
    db.session.commit()
    return jsonify("Vehiculo favorito eliminado"), 200

# PUT Actualizar personaje
@app.route('/persons/<int:id>', methods=['PUT'])
def update_person(id):
    person_query = Person.query.filter_by(id = id).first()
    body = request.get_json()
    # print(person_query.name)
    if "name" in body:
        person_query.name = body["name"]
    if "height" in body:
        person_query.height = body["height"]
    if "eye_color" in body:
        person_query.eye_color = body["eye_color"]
    if "hair_color" in body:
        person_query.hair_color = body["hair_color"]
    if "planet_id" in body:
        person_query.planet_id = body["planet_id"]   
    db.session.commit()
    response_body = {
        "msg": "ok",
        "person update": body
    }

    return jsonify(response_body), 200

# PUT Actualizar planeta
@app.route('/planets/<int:id>', methods=['PUT'])
def update_planet(id):
    planet_query = Planet.query.filter_by(id = id).first()
    body = request.get_json()
    # print(person_query.name)
    if "name" in body:
        planet_query.name = body["name"]
    if "climate" in body:
        planet_query.climate = body["climate"]
    if "diameter" in body:
        planet_query.diameter = body["diameter"]
    if "population" in body:
        planet_query.population = body["population"] 
    db.session.commit()
    response_body = {
        "msg": "ok",
        "planet update": body
    }

    return jsonify(response_body), 200

# PUT Actualizar vehiculos
@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    vehicle_query = Vehicle.query.filter_by(id = id).first()
    body = request.get_json()
    # print(person_query.name)
    if "name" in body:
        vehicle_query.name = body["name"]
    if "length" in body:
        vehicle_query.length = body["length"]
    if "model" in body:
        vehicle_query.model = body["model"]
    if "manufacturer" in body:
        vehicle_query.manufacturer = body["manufacturer"] 
    if "person_id" in body:
        vehicle_query.person_id = body["person_id"]  
    db.session.commit()
    response_body = {
        "msg": "ok",
        "planet update": body
    }

    return jsonify(response_body), 200

# POST Crear uno nuevo personaje
@app.route('/persons', methods=['POST'])
def add_person():
    name = request.json.get("name", None)
    hair_color = request.json.get("hair_color", None)
    eye_color = request.json.get("eye_color", None)
    height = request.json.get("height", None)
    planet_id = request.json.get("planet_id", None)
    person_query = Person.query.filter_by(name = name).first()
    if person_query != None:
        return jsonify({"msg": "There is a person with that name"}), 401

    new_person = Person(name = name, hair_color = hair_color, eye_color = eye_color, height= height, planet_id=planet_id)
    db.session.add(new_person)
    db.session.commit()
    return jsonify("Personaje añadido"), 200

# POST Crear uno nuevo planeta
@app.route('/planets', methods=['POST'])
def add_planet():
    name = request.json.get("name", None)
    climate = request.json.get("climate", None)
    diameter = request.json.get("diameter", None)
    population = request.json.get("population", None)
    planet_query = Planet.query.filter_by(name = name).first()
    if planet_query != None:
        return jsonify({"msg": "There is a planet with that name"}), 401

    new_planet = Planet(name = name, climate = climate, diameter = diameter, population= population)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify("Planeta añadido"), 200

# POST Crear uno nuevo vehiculo
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    name = request.json.get("name", None)
    model = request.json.get("model", None)
    length = request.json.get("length", None)
    manufacturer = request.json.get("manufacturer", None)
    person_id = request.json.get("person_id", None)
    vehicle_query = Vehicle.query.filter_by(name = name).first()
    if vehicle_query != None:
        return jsonify({"msg": "There is a vehicle with that name"}), 401

    new_vehicle = Vehicle(name = name, model = model, length = length, manufacturer= manufacturer, person_id=person_id)
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify("Vehiculo añadido"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
