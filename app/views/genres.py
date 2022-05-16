from flask import request
from flask_restx import Resource, Namespace


from app.models import GenreSchema, Genre

genre_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


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
