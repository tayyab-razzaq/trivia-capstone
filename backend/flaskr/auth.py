"""Module for auth of app."""

from functools import wraps

from flaskr.constants import STATUS_UNAUTHORIZED


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
            # token = get_token_auth_header()
            # payload = verify_decode_jwt(token)
            # check_permissions(permission, payload)
            # return function(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
