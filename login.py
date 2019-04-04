import jwt
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, inputs

from db import User
from helpers import build_jwt, verify_jwt

app = Flask('login')
api = Api(app)


class Login(Resource):

    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', help="Username does not appear to be valid")
        self.parser.add_argument('password', help="Users Password does not appear to be valid")

        super().__init__(*args, **kwargs)

    def get(self):
        """ takes the jwt and decodes it returning the payload """
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return {'error': 'no token'}

        # strip out the Bearer part of the token.
        auth_token = str(auth_token).replace('Bearer ', '')

        try:
            payload = verify_jwt(auth_token)
            return {
                'token': auth_token,
                'payload': payload,
            }
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            app.logger.exception(e)
            return {
                'error': f"{type(e).__name__}:{str(e)}",
                'payload': jwt.decode(auth_token.encode(), verify=False)
            }

    def post(self):
        args = self.parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            user = User.authenticate(username, password)
            return {
                'token': build_jwt(user.token_payload)
            }
        except ValueError as e:
            return {
                'error': f'{e}'
            }


api.add_resource(Login, '/')

# local run
if __name__ == '__main__':
    app.run(debug=True)
