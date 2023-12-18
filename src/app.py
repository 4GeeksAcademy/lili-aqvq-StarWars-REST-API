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
from models import db, User, People, Planets, Favorite_People, Favorite_Planets
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



# -------------------------------------------------- PEOPLE --------------------------------------------------
@app.route('/people', methods=['GET'])  #Listar todos los registros de people en la base de datos
def get_all_people():
    #hago un query all para retornar todas las columnas de la tabla people
    people_query = People.query.all()

    #hago un for in para luego retornarlo en formato json con jsonify
    people_list = [{
        "id": people.id,
        "name": people.name,
        "description": people.description,
        "height": people.height,
        "mass": people.mass,
        "hair_color": people.hair_color,
        "skin_color": people.skin_color,
        "eye_color": people.eye_color,
        "birth_year": people.birth_year,
        "gender": people.gender

    }
        for people in people_query]

    return jsonify(people_list), 200



@app.route('/people/<int:people_id>', methods=['GET'])  #Listar la información de una sola people
def get_people_by_id(people_id):
    #hago un query.get para traer el id del personaje para luego devolverlo en formato json
    people_query = People.query.get(people_id)
    if people_query:
        return jsonify({
            "id": people_query.id,
            "name": people_query.name,
            "description": people_query.description,
            "height": people_query.height,
            "mass": people_query.mass,
            "hair_color": people_query.hair_color,
            "skin_color": people_query.skin_color,
            "eye_color": people_query.eye_color,
            "birth_year": people_query.birth_year,
            "gender": people_query.gender,
        }), 200
    # en caso de que el id de ese personaje no exista se retorna un mensaje de error 
    else:
        return jsonify ({"msg": "Character not found"}), 404



# -------------------------------------------------- PLANETS --------------------------------------------------
    
@app.route('/planets', methods=['GET'])  #Listar todos los registros de planets en la base de datos
def get_all_planets():
    #hago un query all para retornar todas las columnas de la tabla planets
    planets_query = Planets.query.all()

    #hago un for in para luego retornarlo en formato json con jsonify
    planets_list = [{
        "id": planets.id,
        "name": planets.name,
        "diameter": planets.diameter,
        "rotation_period": planets.rotation_period,
        "orbital_period": planets.orbital_period,
        "gravity": planets.gravity,
        "population": planets.population,
        "climate": planets.climate,
        "terrain": planets.terrain,
        "surface_water": planets.surface_water

    }
        for planets in planets_query]

    return jsonify(planets_list), 200


@app.route('/planets/<int:planets_id>', methods=['GET'])  #Listar la información de una sola planets
def get_planets_by_id(planets_id):
     #hago un query.get para traer el id del personaje para luego devolverlo en formato json
    planets_query = Planets.query.get(planets_id)
    if planets_query:
        return jsonify({
            "id": planets_query.id,
            "name": planets_query.name,
            "diameter": planets_query.diameter,
            "rotation_period": planets_query.rotation_period,
            "orbital_period": planets_query.orbital_period,
            "gravity": planets_query.gravity,
            "population": planets_query.population,
            "climate": planets_query.climate,
            "terrain": planets_query.terrain,
            "surface_water": planets_query.surface_water
        }), 200
    # en caso de que el id de ese planeta no exista se retorna un mensaje de error 
    else:
        return jsonify ({"msg": "Planet not found"}), 404



# -------------------------------------------------- USERS --------------------------------------------------
@app.route('/users', methods=['GET']) #Listar todos los usuarios del blog
def get_all_users():
    all_users = User.query.all()
    list_of_users = [{
        'id' : user.id,
        'username' : user.username,
        'email' : user.email,

    } for user in all_users]

    return jsonify(list_of_users), 200




@app.route('/users/<int:user_id>/favorites') #[GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
def get_all_favorites(user_id):
    user_query = User.query.filter_by(id = user_id).first()

    #me aseguro de que el usuario exista en la base datos
    if user_query:

        #hago un blucle for accediendo a la tabla favorite planets mediante el foreinkey 
        list_of_favorite_planets = [{
            'user_id' : fav.user_id,
            'username' : user_query.username,
            'planet_fav_id' : fav.planet_fav_id,
            'planet_name' : Planets.query.filter_by(id = fav.planet_fav_id).first().planet_name,

        } for fav in user_query.favorite_planets]

        #hago un blucle for accediendo a la tabla favorite people mediante el foreinkey
        list_of_favorite_people = [{
            'user_id' : fav.user_id,
            'username' : user_query.username,
            'people_fav_id' : fav.people_fav_id,
            'people_name' : People.query.filter_by(id = fav.people_fav_id).first().people_name,

        } for fav in user_query.favorite_people] 

        #en caso de que el usuario no tenga favoritos retorno el siguiente mensaje
        if len(list_of_favorite_people) == 0 and len(list_of_favorite_planets) == 0:
            return jsonify({'msg': 'this user doesn`t have favorite planets nor characters'}), 400 
        
        #retorno un objeto en formato json de forma ordenada
        return jsonify( {
                         'planets_fav_list' : list_of_favorite_planets,
                         'people_fav_list' : list_of_favorite_people
                          }), 200
    
    else :
        #en caso de que el usuario no exista 
        return jsonify({'msg' : 'this user does not exist'}), 404
    




#-----------------------------------POST AND DELETE FAVORITES-----------------------------------
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST']) #[POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el planet id = planet_id.
def add_favorite_planet(user_id, planet_id):
    user_exists_db = User.query.get(user_id)
    planet_exists_db = Planets.query.get(planet_id)
    user_and_planet_exist_table = Favorite_Planets.query.filter_by(planet_fav_id= planet_id, user_id = user_id).first()

    #me aseguro de que el usuario y el planeta existan en la base de datos para poder agregarlos
    if user_exists_db and planet_exists_db:
            
         #mientras el planeta no exista en la tabla de planetas favoritos        
            if not user_and_planet_exist_table:

                new_fav_planet = Favorite_Planets(user_id = user_exists_db.id, planet_fav_id = planet_exists_db.id)
                db.session.add(new_fav_planet)
                db.session.commit()

                return jsonify({
                    'planet_id' : planet_exists_db.id,    
                    'planet_fav_name' : planet_exists_db.planet_name,
                    'username' : user_exists_db.username,
                    'user_id' : user_exists_db.id,                  
                })
            else:
                return jsonify({
                    'msg' : 'that planet already exists in your favorites'
                }), 400
        
    else:
        return jsonify({'msg' : 'the planet or the user does not exists'}), 404


@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST']) # [POST] /favorite/people/<int:people_id> Añade una nueva people favorita al usuario actual con el people.id = people_id
def add_favorite_people(user_id, people_id):
    user_exists_db = User.query.get(user_id)
    people_exists_db = People.query.get(people_id)
    user_and_people_exist_table = Favorite_People.query.filter_by(people_fav_id= people_id, user_id = user_id).first()

    #me aseguro de que el usuario y el personaje existan en la base de datos para poder agregarlos
    if user_exists_db and people_exists_db:
            
         #mientras el personaje no exista en la tabla de personajes favoritos        
            if not user_and_people_exist_table:

                new_fav_people = Favorite_People(user_id = user_exists_db.id, people_fav_id = people_exists_db.id)
                db.session.add(new_fav_people)
                db.session.commit()

                return jsonify({
                    'people_id' : people_exists_db.id,    
                    'people_fav_name' : people_exists_db.people_name,
                    'username' : user_exists_db.username,
                    'user_id' : user_exists_db.id,                  
                })
            else:
                return jsonify({
                    'msg' : 'that people already exists in your favorites'
                }), 400
        
    else:
        return jsonify({'msg' : 'the people or the user does not exists'}), 404
    


# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id`
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet_by_id(user_id, planet_id):
    user_exists_db = User.query.get(user_id)
    planet_exists_db = Planets.query.get(planet_id)
    user_and_planet_exist_table = Favorite_Planets.query.filter_by(planet_fav_id= planet_id, user_id = user_id).first()

    #me aseguro de que el usuario y el planeta existan en la base de datos para poder eliminarlos
    if user_exists_db and planet_exists_db:
            
         #mientras el planeta exista en la tabla de planetas favoritos        
            if user_and_planet_exist_table:

                db.session.delete(user_and_planet_exist_table)
                db.session.commit()

                return jsonify({
                    'msg' : 'the planet was deleted from your favorites'
                })
            else:
                return jsonify({
                    'msg' : 'that planet does not exists in your favorites'
                }), 400
        
    else:
        return jsonify({'msg' : 'the planet or the user does not exists'}), 404
    

# [DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id
@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people_by_id(user_id, people_id):
    user_exists_db = User.query.get(user_id)
    people_exists_db = People.query.get(people_id)
    user_and_people_exist_table = Favorite_People.query.filter_by(people_fav_id= people_id, user_id = user_id).first()

    #me aseguro de que el usuario y el personaje existan en la base de datos para poder eliminarlos
    if user_exists_db and people_exists_db:
            
         #mientras el personaje exista en la tabla de personajes favoritos        
            if user_and_people_exist_table:

                db.session.delete(user_and_people_exist_table)
                db.session.commit()

                return jsonify({
                    'msg' : 'the people was deleted from your favorites'
                })
            else:
                return jsonify({
                    'msg' : 'that people does not exists in your favorites'
                }), 400
        
    else:
        return jsonify({'msg' : 'the people or the user does not exists'}), 404






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
