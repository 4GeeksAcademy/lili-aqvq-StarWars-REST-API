from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    #COLUMNAS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #RELATIONSHIPS
    favorite_planets = db.relationship('Favorite_Planets', backref='user', lazy=True)
    favorite_people = db.relationship('Favorite_People', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    #COLUMNAS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(550), nullable=False)
    height = db.Column(db.String(25), nullable=False)
    mass = db.Column(db.String(25), nullable=False)
    hair_color = db.Column(db.String(25), nullable=False)
    skin_color = db.Column(db.String(25), nullable=False)
    eye_color = db.Column(db.String(25), nullable=False)
    birth_year = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    #RELATIONSHIPS
    favorite = db.relationship('Favorite_People', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "height": self.height,
            "mass": self.mass,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }
    
class Planets(db.Model):
    #COLUMNAS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    diameter = db.Column(db.String(25), nullable=False)
    rotation_period = db.Column(db.String(25), nullable=False)
    orbital_period = db.Column(db.String(25), nullable=False)
    gravity = db.Column(db.String(55), nullable=False)
    population = db.Column(db.String(25), nullable=False)
    climate = db.Column(db.String(25), nullable=False)
    terrain = db.Column(db.String(25), nullable=False)
    surface_water = db.Column(db.String(25), nullable=False)
    #RELATIONSHIPS
    favorite = db.relationship('Favorite_Planets', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }
    
class Favorite_People(db.Model):
    #COLUMNAS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #RELATIONSHIPS
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Favorite_People %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id
        }
    
class Favorite_Planets(db.Model):
    #COLUMNAS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #RELATIONSHIPS
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Favorite_Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "user_id": self.user_id
        }



