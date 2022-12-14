import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
from auth import AuthError, requires_auth
from models import *
ASSISTANT_TOKEN=os.environ['ASSISTANT_TOKEN']
DIRECTOR_TOKEN=os.environ['DIRECTOR_TOKEN']
PRODUCER_TOKEN=os.environ['PRODUCER_TOKEN']

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = '123454321a@'
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    #db_drop_and_create_all()
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        return response

    """
        Special login functions
    """
    # login Assistant route
    @app.route('/loginAssistant', methods=['GET'])
    def login_Assistant():
        return jsonify({
            'success': True,
            'Token': [ASSISTANT_TOKEN]
        }), 200

    # login Producer route
    @app.route('/loginProducer', methods=['GET'])
    def login_Producer():
        return jsonify({
            'success': True,
            'Token': [PRODUCER_TOKEN]
        }), 200

    # login Director route
    @app.route('/loginDirector', methods=['GET'])
    def login_Director():
        return jsonify({
            'success': True,
            'Token': [DIRECTOR_TOKEN]
        }), 200

    """
        End Special login functions
    """
    # get_movies route - get all the movies in the database
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
                }), 200
        except Exception:
            abort(500)

    # add_movie route - post a movie in the database
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        print("Add movie init")
        data = request.get_json()
        print("request.get_json")
        movie = Movie(
            title=data['title'],
            release_date=data['release_date']
            )
        print("movie created")
        if movie.title == '' or movie.release_date == '':
            abort(422)

        try:
            print("ready to insert movie")
            movie.insert()
            print("insertion done")
            return jsonify({
                'success': True,
                'movie': movie.format()
                }), 200
        except Exception:
            abort(500)

    # delete_movie route - delete an entry in movie in the database
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movieLocal = Movie.query.filter(Movie.id == id).one_or_none()
        if movieLocal is None:
           abort(404)
        else:
            try:
                movieLocal.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                    }), 200
            except Exception:
                db.session.rollback()
                abort(500)

    # update_movie route - PATCH an entry in movie in the database
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        dataLocal = request.get_json()
        movieLocal = Movie.query.filter(Movie.id == id).one_or_none()
        if movieLocal is None:
            abort(404)
        else:
            movieLocal.title = (dataLocal['title'] if dataLocal['title']
                           else movieLocal.title)

            movieLocal.release_date = (dataLocal['release_date'] if
                                  dataLocal['release_date'] else
                                  movieLocal.release_date)

        try:
            movieLocal.update()

            return jsonify({
                'success': True,
                'movie': [movieLocal.format()]
                }), 200
        except Exception:
            abort(500)


    # get_actors endpoints - get list of all actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            return jsonify({
                            'success': True,
                            'actors': [actor.format() for actor in actors]
                            }), 200
        except Exception:
            abort(500)

    # add_actor endpoints - add an actor to the list
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        data = request.get_json()
        actor = Actor(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            movie_id=data['movie_id']
            )
        if actor.name == '' or actor.age == '' or actor.gender == '':
            abort(422)
        try:
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
                }), 200
        except Exception:
            abort(500)

    # delete_actor endpoints - delete an actor from the database
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        else:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                    }), 200
            except Exception:
                db.session.rollback()
                abort(500)


    # update_actor endpoints - add an actor to the database
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        new_info = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        else:
            actor.name = (new_info['name'] if new_info['name']
                          else Actor.name)
            actor.age = (new_info['age'] if new_info['age']
                         else actor.age)
            actor.gender = (new_info['gender'] if new_info['gender']
                            else actor.gender)
            actor.movie_id = (new_info['movie_id'] if new_info['movie_id']
                              else actor.movie_id)
            try:
                actor.update()
                return jsonify({
                    'success': True,
                    'actor': [actor.format()]
                    }), 200
            except Exception:
                abort(500)


    # default route
    @app.route('/')
    def index():
        print("landed in default")
        return render_template('index.html')


    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request, please check your inputs"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found."
            }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Sorry, there's a problem on our end."
            }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable. Check your input.'
          }), 422

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Permission not found.",
                }), 403

    @app.errorhandler(AuthError)
    def auth_error(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
