import markdown
import os
import uuid
import shelve

# Import the framework
from flask import Flask, g, request, url_for, jsonify
from flask_restful import Resource, Api, reqparse
from flask_api import FlaskAPI, status, exceptions
from py2neo import Graph, Node, Relationship


graph = Graph("http://neo4j:7474/db/data/")

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class Person(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        node = Node("Person", id=args['id'], name=args['name'], age=args['age'])
        graph.create(node)

        return {'message': 'Person registered', 'data': args}, 201


class BidirectionalRelation(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('relation', required=True)
        parser.add_argument('first_id', required=True)
        parser.add_argument('second_id', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        first_node = graph.find_one("Person", "id", args['first_id'])
        second_node = graph.find_one("Person", "id", args['second_id'])

        relation_1 = Relationship(first_node, args['relation'], second_node)
        relation_2 = Relationship(second_node, args['relation'], first_node)
        graph.create(relation_1)
        graph.create(relation_2)

        return {'message': 'Relationship registered', 'data': args}, 201


api.add_resource(Person, '/person')
api.add_resource(BidirectionalRelation, '/relation')
