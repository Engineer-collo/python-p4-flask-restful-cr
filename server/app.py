#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Newsletter RESTful API"}
        return make_response(response_dict, 200)

api.add_resource(Home, '/')


# GET and POST requests for the /newsletters endpoint
class Newsletters(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        return make_response(response_dict_list, 200)

    def post(self):
        data = request.get_json()
        new_newsletter = Newsletter(title=data['title'], body=data['body'])

        db.session.add(new_newsletter)
        db.session.commit()

        return make_response(new_newsletter.to_dict(), 201)

api.add_resource(Newsletters, '/newsletters')


# GET request for the /newsletters/<id> endpoint
class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.get(id)
        
        if newsletter is None:
            return make_response({"error": f"Newsletter {id} not found."}, 404)

        return make_response(newsletter.to_dict(), 200)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')  # Moved up

if __name__ == '__main__':
    app.run(port=5555, debug=True)
