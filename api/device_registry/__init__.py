import markdown
import os
import uuid
import shelve

# Import the framework
from flask import Flask, g, request, url_for, jsonify
from flask_restful import Resource, Api, reqparse
from flask_api import FlaskAPI, status, exceptions
from py2neo import Graph, Node, Relationship
from json import dumps

from .functions import get_people_count, get_disease_count, get_infected_count


# graph = Graph("http://neo4j:7474/db/data/")
graph = Graph(os.environ['NEO4J_URL'])

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
    def get(self):
        count = get_people_count(graph)

        return {'message': 'Success', 'count': count}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        id = get_people_count(graph)
        node = Node("Person", id=id, name=args['name'], age=args['age'])
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

        first_node = graph.find_one("Person", "id", int(args['first_id']))
        second_node = graph.find_one("Person", "id", int(args['second_id']))

        relation_1 = Relationship(first_node, args['relation'], second_node)
        relation_2 = Relationship(second_node, args['relation'], first_node)
        graph.create(relation_1)
        graph.create(relation_2)

        return {'message': 'Relationship registered', 'data': args}, 201


class Disease(Resource):
    def get(self):
        count = get_disease_count(graph)

        return {'message': 'Success', 'count': count}, 200


    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('spread_type', required=True)
        parser.add_argument('infected_id', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        id = get_disease_count(graph)
        node = Node("Disease", id=id, name=args['name'], spread_type=args['spread_type'], current_infected=1)
        infected = graph.find_one("Person", "id", int(args['infected_id']))
        relation = Relationship(node, "INFECTS", infected)
        graph.create(node)
        graph.create(relation)

        return {'message': 'Disease registered', 'data': args, 'id': id}, 201


class DiseaseSpread(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        disease_node = graph.find_one("Disease", "id", int(args['id']))
        spread_type = disease_node.properties["spread_type"]
        rel_affected = ""

        if spread_type == "fluids":
            rel_affected = ":FAMILY"
        if spread_type == "touch":
            rel_affected = ":WORK|FAMILY"
        if spread_type == "air":
            rel_affected = ":NEIGHBOR|WORK|FAMILY"

        cypher = graph.cypher
        query = "MATCH (d:Disease {id:" + args['id'] + "})-[:INFECTS]-(p:Person), (p)-[" + rel_affected + "]->(a) MERGE (d)-[s:INFECTS]->(a)"
        cypher.execute(query)
        current_infected = get_infected_count(graph, args['id'])
        disease_node.properties["current_infected"] = current_infected
        disease_node.push()

        return {'message': 'Disease spreaded', 'data': rel_affected}, 201


class DiseaseCure(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        count = get_infected_count(graph, args['id'])
        return {'message': 'Success', 'count': count}, 200


    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        cypher = graph.cypher
        query = "MATCH (d:Disease {id:" + args['id'] + "})-[r:INFECTS]-(p:Person) WITH d,r,p limit 1 DELETE r MERGE (d)-[:CURED]->(p)"
        cypher.execute(query)

        disease_node = graph.find_one("Disease", "id", int(args['id']))
        disease_node.properties["current_infected"] = disease_node.properties["current_infected"] - 1
        disease_node.push()

        return {'message': 'Disease cured', 'data': args}, 201

api.add_resource(Person, '/person')
api.add_resource(BidirectionalRelation, '/relation')
api.add_resource(Disease, '/disease')
api.add_resource(DiseaseSpread, '/spread')
api.add_resource(DiseaseCure, '/cure')
