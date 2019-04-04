import datetime
import json
import os
import jwt
from typing import Dict, Any

# SETTINGS

SECRET_KEY = os.environ['SECRET_KEY']
JWT_EXPIRATION_MINUTES = float(os.environ['JWT_EXPIRATION_MINUTES'])
JWT_DOMAIN = 'benjamin.dog'


# JWT HELPERS


class JSONDateTimeEncoder(json.JSONEncoder):
    """ setup a json encoder to convert datetime objects """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return super().default(obj)


def build_jwt(payload: dict) -> str:
    """ return a jwt token for the payload """
    if 'sub' not in payload.keys():
        raise ValueError('sub not in payload keys')
    jwt_fields = {
        'iss': JWT_DOMAIN,
        'sub': None,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
        **payload
    }
    return jwt.encode(jwt_fields, key=SECRET_KEY, json_encoder=JSONDateTimeEncoder).decode(encoding='UTF-8')


def verify_jwt(token):
    """ verity the jwt token """
    return jwt.decode(token.encode(), SECRET_KEY)


# AWS LAMBDA TYPE HELPERS


LambdaDict = Dict[str, Any]


class LambdaCognitoIdentity(object):
    cognito_identity_id: str
    cognito_identity_pool_id: str


class LambdaClientContextMobileClient(object):
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str


class LambdaClientContext(object):
    client: LambdaClientContextMobileClient
    custom: LambdaDict
    env: LambdaDict


class LambdaContext(object):
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: LambdaCognitoIdentity
    client_context: LambdaClientContext

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        return 0
