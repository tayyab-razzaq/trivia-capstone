"""Module for auth of app."""
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
