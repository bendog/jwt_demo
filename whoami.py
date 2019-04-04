from datetime import datetime

import jwt
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask('whoami')
api = Api(app)


class WhoAmI(Resource):

    def get(self):
        """ takes the jwt and decodes it returning the payload """
        try:
            auth_token = request.headers.get('Authorization')
            if not auth_token:
                raise ValueError("No token provided")
            auth_token = str(auth_token).replace('Bearer ', '')
            payload = jwt.decode(auth_token.encode(), verify=False)
            return {
                'payload': dict(payload),
                'extra': {
                    'iat_string_utc': datetime.utcfromtimestamp(payload.get('iat')).isoformat(),
                    'exp_string_utc': datetime.utcfromtimestamp(payload.get('exp')).isoformat(),
                    'iat_string_local': datetime.fromtimestamp(payload.get('iat')).isoformat(),
                    'exp_string_local': datetime.fromtimestamp(payload.get('exp')).isoformat(),
                }
            }
        except Exception as e:
            return {
                'error': f"{type(e).__name__}:{str(e)}"
            }


api.add_resource(WhoAmI, '/')


# local run
if __name__ == '__main__':
    app.run(debug=True)
