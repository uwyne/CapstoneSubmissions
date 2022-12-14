##Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

##Models:
	Movies with attributes title and release date
	Actors with attributes name, age and gender
##Endpoints:
	GET /actors and /movies
	DELETE /actors/ and /movies/
	POST /actors and /movies and
	PATCH /actors/ and /movies/
##Roles:
	#Casting Assistant
		Can view actors and movies
	#Casting Director
		All permissions a Casting Assistant has and…
		Add or delete an actor from the database
		Modify actors or movies
	#Executive Producer
		All permissions a Casting Director has and…
		Add or delete a movie from the database
	#Tests:
		One test for success behavior of each endpoint
		One test for error behavior of each endpoint
		At least two tests of Role based access control (RBAC) for each role


### How to setup authentication
This project comes with three auth0 JWT tokens for Producer, Director and Assistant. These are valid for 30 days, and will expire after that.

###instructions usage from Heroku
1. Go to website https://castingdb-wyne.herokuapp.com/
2. Login into the role that you want to use
3. You can get movies and actors stored in database by just pressing the correct login button
4. For post you can  add information that you need.
		MOVIES
			Add Movie name
			Add release date
		actors
				Add name, age, Gender, and movie ID that actor has worked in
				Please note that movie ID must exist in the database.
	5. To delete a movie or an actor, just enter the movie or actor ID and press corresponding delete button
	6. To patch a movie or an actor, add the movie or actor ID and also add the details that you want to change
	Please note that deleting a movie will also delete the related actor from the database.

	The Result window shows raw XML data that shows what information is being returned.


### Installing and Running

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
	```bash
		pip install -r requirements.txt
	```
	This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
	pyjwt==1.7.1 is a Python library which allows you to encode and decode JSON Web Tokens (JWT
	flask==1.1.2 is a lightweight backend microservices framework. Flask is required to handle requests and responses.
	Jinja2<3.0.0 - is a web template engine for the Python programming languag
	SQLAlchemy - is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py
	Flask-CORS - is the extension we'll use to handle cross origin requests from our frontend server.

5. run ```source setup.sh``` to set the user jwts, auth0 credentials

6. Database Setup

  ```
  psql casting < castingdbdump.pgsql
  ```

7. Run the development server:
  ```
  $ export FLASK_APP=app
  $ export FLASK_ENV=development # enables debug mode
  $ flask run
  ```


## Testing
To run the tests, run
```
dropdb casting_test
createdb casting_test
psql castingtest < castingdbdump.pgsql
python -m unittest test_app.py
```

## API Reference

### Endpoints

#### GET '/movies'
- General:
    - Return all movies in the database
    - Role Authorized: Assistant, Director, Producer
- Example: ```curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/movies```
```
	{
	  "movies": [
	    {
	      "id": 4,
	      "release_date": "Thu, 23 Jun 2022 06:00:00 GMT",
	      "title": "Thor: Love and Thunder"
	    },
	    {
	      "id": 16,
	      "release_date": "Fri, 10 Jun 2022 06:00:00 GMT",
	      "title": "Jurassic World Dominion"
	    },
	    {
	      "id": 3,
	      "release_date": "Fri, 16 Dec 2022 06:00:00 GMT",
	      "title": "Avatar: The Way of Water"
	    },
	    {
	      "id": 17,
	      "release_date": "Thu, 23 Jun 2022 16:00:00 GMT",
	      "title": "Thor: Love and Thunder 59"
	    },
	    {
	      "id": 20,
	      "release_date": "Sat, 12 Nov 2022 06:00:00 GMT",
	      "title": "New movie 2"
	    }
	  ],
	  "success": true
	}
```
#### GET '/actors'
- General:
    - Return all actors in the database
    - Role Authorized: Assistant, Director, Producer
- Example: ```curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/actors```
```
{
  "actors": [
    {
      "age": 44,
      "gender": "F",
      "id": 3,
      "movie_id": 3,
      "name": "Zoe Saldana"
    },
    {
      "age": 47,
      "gender": "F",
      "id": 11,
      "movie_id": 3,
      "name": "Angelina Jolie"
    },
    {
      "age": 22,
      "gender": "M",
      "id": 13,
      "movie_id": 20,
      "name": "Angeline Jolie 19"
    }
  ],
  "success": true
}

```

#### POST '/movies'
- General:
    - Add a new movie. The new movie must have all four information.
    - Role Authorized: Producer
- Example: ```curl -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"title": "A few good men", "release_date": "1992-12-11"}' http://127.0.0.1:5000/movies```
```
{
  "movie": {
    "id": 21,
    "release_date": "Fri, 11 Dec 1992 06:00:00 GMT",
    "title": "A few good men"
  },
  "success": true
}
```

#### POST '/actors'
- General:
    - Add a new actor. The new movie must have all four information.
    - Role Authorized: Director, Producer
- Example: ```curl -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"name": "Tom Cruise", "age": 60, "gender": "M", "movie_id": 21}' http://127.0.0.1:5000/actors```

```
{
  "actor": {
    "age": 60,
    "gender": "M",
    "id": 14,
    "movie_id": 21,
    "name": "Tom Cruise"
  },
  "success": true
}
```

#### PATCH '/movies/<int:id>'
- General:
    - Update some information of a movie based on a payload.
    - Roles authorized : Director, Producer.
- Example: ```curl http://127.0.0.1:5000/movies/21 -X PATCH -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{ "title": "", "release_date": "2022-12-01" }'```
```
{
  "movie": [
    {
      "id": 21,
      "release_date": "Thu, 01 Dec 2022 06:00:00 GMT",
      "title": "A few good men"
    }
  ],
  "success": true
}

```

#### PATCH '/actors/<int:id>'
- General:
    - Update some information of an actor based on a payload.
    - Roles authorized : Director, Producer.
- Example: ```curl -X PATCH - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"name": "", "age": 88, "gender": "M", "movie_id": ""}' http://127.0.0.1:5000/actors/14```
```
{
  "actor": [
    {
      "age": 88,
      "gender": "M",
      "id": 14,
      "movie_id": 21,
      "name": "Tom Cruise"
    }
  ],
  "success": true
}
```

#### DELETE '/movis/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Executive Producer.
- Example: ```curl -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -X DELETE http://127.0.0.1:5000/movies/21```
```
{
  "delete": 21,
  "success": true
}

```

#### DELETE '/actors/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -X DELETE http://127.0.0.1:5000/actors/14```
```
{
  "delete": 14,
  "success": true
}

```

### Error Handling
Errors are returned in the following json format:
```
{
    'success': False,
    'error': 404,
    'message': 'Resource not found. Input out of range.'
}
```
The API returns 6 types of errors:
- 400: Bad Request, please check your inputs
- 404: resource not found.
- 403: Permission not found.
- 422: unprocessable. Check your input.
- 500: Sorry, there's a problem on our end.
- AuthError:
					401-Token expired.
					401-Incorrect claims. Please, check the audience and issuer.
					400-Unable to parse authentication token.
					400-Unable to find the appropriate key.

## Author
- Usman Wyne
