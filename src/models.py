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
    diameter = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250), nullable=True)
    persons = db.relationship('Person', backref='planet', lazy=True)
    favourites = db.relationship('Favourite', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population,
            # do not serialize the password, its a security breach
        }


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    height = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
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
            "height": self.height,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "planet of birth": planet.serialize()
            
            # do not serialize the password, its a security breach
        }


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    model = db.Column(db.String(250), nullable=True)
    length = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    favourites = db.relationship('Favourite', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        person = Person.query.filter_by(id = self.person_id).first()
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "length": self.length,
            "manufacturer": self.manufacturer,
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
      