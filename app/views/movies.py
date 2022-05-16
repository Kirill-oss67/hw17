from flask import request
from flask_restx import Resource, Namespace

from app.models import MovieSchema, Movie

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            genre_id = request.args.get('genre_id')  # Получение id жанра
            director_id = request.args.get('director_id')  # Получение id режиссера
            if director_id and genre_id:
                movies = Movie.query.filter(Movie.director_id == director_id).filter(Movie.genre_id == genre_id)
                return movies_schema.dump(movies)
            if genre_id:
                movies_by_genre = Movie.query.filter(
                    Movie.genre_id == genre_id)  # Получение фильмов по запросу где жанр id в модели равен полученному id (шаг 4)
                return movies_schema.dump(movies_by_genre)
            if director_id:
                movies_by_director = Movie.query.filter(
                    Movie.director_id == director_id)  # Получение фильмов по запросу где режиссер id в модели равен полученному id(шаг 3)
                return movies_schema.dump(movies_by_director)
            else:
                all_movies = Movie.query.all()
                return movies_schema.dump(all_movies), 200
        except Exception:
            return 'неверное значение', 404


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        return movie_schema.dump(movie), 200
