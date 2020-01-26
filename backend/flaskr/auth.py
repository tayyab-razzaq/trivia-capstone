"""Module for auth of app."""

import json
from functools import wraps
from urllib.request import urlopen

from flask import request

from jose import jwt


from flaskr.constants import (
    STATUS_UNAUTHORIZED, MISSING_AUTHORIZATION, MISSING_BEARER, MISSING_TOKEN,
    MISSING_BEARER_TOKEN, ERROR_MESSAGES, TOKEN_EXPIRED,
    INCORRECT_CLAIMS, UNABLE_TO_PARSE, STATUS_BAD_REQUEST,
    INAPPROPRIATE_KEY, AUTHORIZATION_MALFORMED
)

AUTH0_DOMAIN = 'dummy'
ALGORITHMS = ['dummy']
API_AUDIENCE = 'dummy'


class AuthError(Exception):
    """A standardized way to communicate auth failure modes."""

    def __init__(self, error, status_code):
        """
        Init method of class.

        :param error:
        :param status_code:
        """
        self.error = error
        self.status_code = status_code


def raise_auth_error(message, error=STATUS_UNAUTHORIZED):
    """
    Raise auth error with given message.

    :param message:
    :param error:
    :return:
    """
    raise AuthError({
        'success': False,
        'message': message,
        'error': error
    }, error)


def get_token_auth_header():
    """
    Get token from authorization header and raise error is header is incorrect.

    :return:
    """
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise_auth_error(MISSING_AUTHORIZATION)

    authorization_parts = authorization.split(' ')
    if authorization_parts[0].lower() != 'bearer':
        raise_auth_error(MISSING_BEARER)

    elif len(authorization_parts) == 1:
        raise_auth_error(MISSING_TOKEN)

    elif len(authorization_parts) > 2:
        raise_auth_error(MISSING_BEARER_TOKEN)

    token = authorization_parts[1]
    return token


def verify_decode_jwt(token):
    """
    Verify if jwt can be decoded properly and is not tempered.

    :param token:
    :return:
    """
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise_auth_error(AUTHORIZATION_MALFORMED)

    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    rsa_key = {}

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise_auth_error(TOKEN_EXPIRED)

        except jwt.JWTClaimsError:
            raise_auth_error(INCORRECT_CLAIMS)

        except Exception:
            raise_auth_error(UNABLE_TO_PARSE, STATUS_BAD_REQUEST)

    raise_auth_error(INAPPROPRIATE_KEY, STATUS_BAD_REQUEST)


def check_permissions(permission, payload):
    """
    Check permission against a payload.
    :param permission:
    :param payload:
    :return:
    """
    if 'permissions' in payload and permission in payload['permissions']:
        return True

    raise AuthError({
        'success': False,
        'error': STATUS_UNAUTHORIZED,
        'message': ERROR_MESSAGES[STATUS_UNAUTHORIZED]
    }, STATUS_UNAUTHORIZED)


def requires_auth(permission=''):
    """
    Require Auth method.

    :param permission:
    :return:
    """

    def requires_auth_decorator(function):
        """
        Require Auth decorator.

        :param function:
        :return:
        """

        @wraps(function)
        def wrapper(*args, **kwargs):
            """
            Decorate wrapper method.

            :param args:
            :param kwargs:
            :return:
            """
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return function(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
