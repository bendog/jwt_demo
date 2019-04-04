from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from db import User
from helpers import JSONDataEncoder

app = Flask('users')
api = Api(app)


class MyConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': JSONDataEncoder
    }


app.config.from_object(MyConfig)


class Users(Resource):

    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('github', type=str, required=True)
        self.parser.add_argument('groups', type=str, required=True, action="append")

        super().__init__(*args, **kwargs)

    def get(self):
        response = []
        for user in User.scan():
            response.append(user.token_payload)
        return {
            'users': response
        }

    def post(self):
        args = self.parser.parse_args()
        print(args)
        user = User(
            username=args.get('username'),
            password=args.get('password'),
            github=args.get('github'),
            groups=set(args.get('groups'))
        )
        user.save()
        user.refresh()
        return {
            "user": user.token_payload
        }


api.add_resource(Users, '/')

# local run
if __name__ == '__main__':
    app.run(debug=True)
