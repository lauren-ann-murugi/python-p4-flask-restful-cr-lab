#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


# -------------------------
# Routes
# -------------------------
class Plants(Resource):
    def get(self):
        """Index route: return all plants"""
        plants = [p.to_dict() for p in Plant.query.all()]
        return make_response(plants, 200)

    def post(self):
        """Create route: add a new plant"""
        data = request.get_json()
        new_plant = Plant(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price"),
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)


class PlantByID(Resource):
    def get(self, id):
        """Show route: return plant by id"""
        plant = Plant.query.get_or_404(id)
        return make_response(plant.to_dict(), 200)


# Register endpoints
api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")


if __name__ == '_main_':
    app.run(port=5555, debug=True)