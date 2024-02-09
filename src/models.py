from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favourites = db.relationship('Favourite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    url_img = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    orbital_period = db.Column(db.String(250), nullable=True)
    rotation_period = db.Column(db.String(250), nullable=True)
    persons = db.relationship('Person', backref='planet', lazy=True)
    favourites = db.relationship('Favourite', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "description": self.description,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period
            # do not serialize the password, its a security breach
        }


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    url_img = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    height = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    vehicles = db.relationship('Vehicle', backref='person', lazy=True)
    favourites = db.relationship('Favourite', backref='person', lazy=True)
    

    def __repr__(self):
        return '<Person %r>' % self.id

    def serialize(self):
        planet = Planet.query.filter_by(id = self.planet_id).first()
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "description": self.description,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "planet of birth": planet.serialize()
            
            # do not serialize the password, its a security breach
        }


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    url_img = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    model = db.Column(db.String(250), nullable=True)
    length = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    cargo_capacity = db.Column(db.String(250), nullable=True)
    crew = db.Column(db.String(250), nullable=True)
    max_atmosphering_speed = db.Column(db.String(250), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    favourites = db.relationship('Favourite', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        person = Person.query.filter_by(id = self.person_id).first()
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "description": self.description,
            "model": self.model,
            "length": self.length,
            "manufacturer": self.manufacturer,
            "cargo_capacity": self.cargo_capacity,
            "crew": self.crew,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "driver": person.serialize(),
            # do not serialize the password, its a security breach
        }

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)

    def __repr__(self):
        return '<Favourite %r>' % self.id

    def serialize(self):
        person = Person.query.filter_by(id = self.person_id).first()
        planet = Planet.query.filter_by(id = self.planet_id).first()
        vehicle = Vehicle.query.filter_by(id = self.vehicle_id).first()
        if self.person_id is not None:
            return {
            "id": self.id,
            "user_id": self.user_id,
            "info_person": person.serialize(),
            # do not serialize the password, its a security breach
        }
        elif self.planet_id is not None:
            return {
            "id": self.id,
            "user_id": self.user_id,
            "info_planet": planet.serialize(),
            # do not serialize the password, its a security breach
        }
        else:
            return {
            "id": self.id,
            "user_id": self.user_id,
            "info_vehicle": vehicle.serialize(),
            # do not serialize the password, its a security breach
        }
      