from flask import request
from flask_restx import Resource, Namespace

from app.models import DirectorSchema, Director

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


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
