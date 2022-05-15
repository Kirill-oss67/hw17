# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

db.create_all()


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query.all()
        return genres_schema.dump(all_genres), 200


@genre_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id):
        genre = Genre.query.get(id)
        return genre_schema.dump(genre), 200


@director_ns.route("/")
class DirectorView(Resource):
    def get(self):
        all_directors = Director.query.all()
        return directors_schema.dump(all_directors), 200

@director_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        director = Director.query.get(id)
        return director_schema.dump(director), 200



@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            genre_id = request.args.get('genre_id')  # Получение id жанра
            director_id = request.args.get('director_id')  # Получение id режиссера
            if genre_id:
                movies_by_genre = Movie.query.filter(
                    Movie.genre_id == genre_id)  # Получение фильмов по запросу где жанр id в модели равен полученному id (шаг 4)
                return movies_schema.dump(movies_by_genre)
            elif director_id:
                movies_by_director = Movie.query.filter(
                    Movie.director_id == director_id)  # Получение фильмов по запросу где режиссер id в модели равен полученному id(шаг 3)
                return movies_schema.dump(movies_by_director)
            else:
                all_movies = Movie.query.all()
                return movies_schema.dump(all_movies), 200
        except Exception :
            return 'неверное значение'


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        return movie_schema.dump(movie), 200


if __name__ == '__main__':
    app.run(debug=True)
