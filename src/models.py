from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("User_Favorite", back_populates = "user", uselist = True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        
            # do not serialize the password, its a security breach
        }


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    img = db.Column(db.String(), unique=True, nullable=False)
    characters = db.relationship('Character', back_populates='item')
    planets = db.relationships('Planets', back_populates='item')
    vehicles = db.relationships('Vehicles', back_populates='item')
    favorites = db.relationships('User_Favorite', back_populates='item')

class Character(db.Model):
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    birth_year = db.Column(db.String, unique=False, nullable=False)
    height = db.Column(db.String())
    hair_color = db.Column(db.String(30))
    eye_color = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item', back_populate='characters')
    favorites_character = db.relationship('User_Favorite', back_populate='characters')

    # def __repr__(self):
    #     return '<Characters %r>' % self.character
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.leader,
        }
    
class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(100))
    climate = db.Column(db.String(100))
    population = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item', back_populate='characters')
    favorite_planets = db.relationship('User_Favorite', back_populates = "planets", uselist = True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "favorites": [favorite.serialize() for favorite in self.favorite_planets],
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False)
    model_name = db.Column(db.String(30),)
    manufacturer= db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    length = db.Column(db.String(100), unique=True, nullable=False)

    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String)
    occupation = db.Column(db.String(50))
    favorite_characters = db.relationship("User_Favorite", back_populates = "characters", uselist = True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "occupation": self.occupation
        }

class User_Favorite(db.Model):
    __tablename__ = 'user_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    name_of_favorite = db.Column(db.String(100), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    user = db.relationship('User', back_populates = "favorites")
    planets = db.relationship('Planets', back_populates = "favorites")
    characters = db.relationship('Characters', back_populates = "favorites")
    vehicles = db.relationship('Item', back_populates = "favorites")

    # __table_args__= (db.UniqueConstraint("user_Id", "name_of_favorite", "id", name = "unique_favorite"),)

    # def __repr__(self):
    #     return '<User_favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name_of_favorite": self.name_of_favorite,
            "planets_id": self.characters_id,
            "vehicles_id": self.vehicles_id,
            "user_id": self.vehicles_id,
            # do not serialize the password, its a security breach
        }
    
    