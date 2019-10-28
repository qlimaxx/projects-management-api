import re
from functools import wraps

from flask import g, jsonify

from .enums import Role
from .exceptions import InvalidRoleError


def response_error(message, status_code):
    return jsonify({'error': message}), status_code


def require_role(role):
    def wrapper(func):
        @wraps(func)
        def check_role(*args, **kwargs):
            try:
                roles = list(Role)
                if roles.index(role) > roles.index(Role(g.user.role)):
                    raise InvalidRoleError
            except (ValueError, InvalidRoleError):
                return response_error('Invalid user role.', 403)
            return func(*args, **kwargs)
        return check_role
    return wrapper


def is_valid_email(email):
    if len(email) >= 5:
        return bool(
            re.match(
                r'^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$',
                email))
    return False


def is_valid_hash(_hash):
    if _hash.count('$') < 2:
        return False
    return True
