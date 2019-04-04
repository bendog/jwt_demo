from flask import Flask, request
from flask_restful import Resource, Api, reqparse, inputs


app = Flask('login')
api = Api(app)


class Login(Resource):

    def get(self):
        prices = [
            {'north lake': 123.6}
        ]
        return {
            "fuelwatch": "result",
            'prices': prices
        }


api.add_resource(Login, '/')
