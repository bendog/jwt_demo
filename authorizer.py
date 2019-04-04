import logging
from typing import Union, Optional
import jwt
from helpers import LambdaDict, LambdaContext, SECRET_KEY


def generate_policy(principal_id: Union[int, str, None], effect: str, method_arn: str) -> dict:
    """ return a valid AWS policy response """
    auth_response = {'principalId': principal_id}
    if effect and method_arn:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': method_arn
                }
            ]
        }
        auth_response['policyDocument'] = policy_document
    return auth_response


def decode_auth_token(auth_token: str) -> Optional[dict]:
    """ Decodes the auth token """
    try:
        # remove "Bearer " from the token string.
        auth_token = auth_token.replace('Bearer ', '')
        # decode using system environ $SECRET_KEY, will crash if not set.
        return jwt.decode(auth_token.encode(), SECRET_KEY)
    except jwt.ExpiredSignatureError:
        'Signature expired. Please log in again.'
        return
    except jwt.InvalidTokenError:
        'Invalid token. Please log in again.'
        return


# noinspection PyUnusedLocal
def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    try:
        auth_token = event.get('authorizationToken')
        method_arn = event.get('methodArn')
        if auth_token and method_arn:
            # verify the JWT
            user_details = decode_auth_token(auth_token)
            if user_details:
                # if the JWT is valid and not expired return a valid policy.
                return generate_policy(user_details.get('sub'), 'Allow', method_arn)
    except Exception as e:
        logging.exception(e)
        return {
            'error': f"{type(e).__name__}:{e}"
        }
    return generate_policy(None, 'Deny', method_arn)
