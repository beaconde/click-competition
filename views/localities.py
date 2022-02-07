import flask_praetorian
from flask import request
from flask_restx import abort, Resource, Namespace

from model import Locality, db, LocalitySchema

# namespace declaration
api_locality = Namespace("Localities", "Localities management")

# Controller detailed comments in: users.py


@api_locality.route("/<locality_id>")
class LocalityController(Resource):
    @flask_praetorian.auth_required
    def get(self, locality_id):
        locality = Locality.query.get_or_404(locality_id)
        return LocalitySchema().dump(locality)

    # roles accepted (user with one of these roles)
    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, locality_id):
        locality = Locality.query.get_or_404(locality_id)
        db.session.delete(locality)
        db.session.commit()
        return f"Deleted locality {locality_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, locality_id):
        new_locality = LocalitySchema().load(request.json)
        if str(new_locality.id) != locality_id:
            abort(400, "id mismatch")
        db.session.commit()
        return LocalitySchema().dump(new_locality)


@api_locality.route("/")
class LocalityListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return LocalitySchema(many=True).dump(Locality.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        locality = LocalitySchema().load(request.json)
        db.session.add(locality)
        db.session.commit()
        return LocalitySchema().dump(locality), 201
