from functools import wraps
from uengine.utils import get_user_from_app_context
from uengine.errors import AuthenticationError


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        u = get_user_from_app_context()
        if u is None:
            raise AuthenticationError()
        return func(*args, **kwargs)
    return wrapper
