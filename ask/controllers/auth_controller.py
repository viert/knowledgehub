import os
from flask import Blueprint, g, session, request
from uengine.errors import AuthenticationError
from uengine.context import ctx
from ask.models import Token, User


class AuthController(Blueprint):
    def __init__(self, *args, **kwargs):
        self.require_auth = kwargs.get("require_auth") or False
        if "require_auth" in kwargs:
            del kwargs["require_auth"]
        Blueprint.__init__(self, *args, **kwargs)
        self.before_request(self.set_current_user)

    @staticmethod
    def _get_user_from_authorization_header():
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"].split()
            if len(auth) == 2 and auth[0] == "Token":
                token = Token.cache_get(auth[1])
                if token is not None and not token.expired:
                    token.prolongate()
                    return token.user
        return None

    @staticmethod
    def _get_user_from_session():
        user_id = session.get("user_id")
        if user_id:
            user = User.cache_get(user_id)
            return user
        return None

    @staticmethod
    def _get_user_from_x_api_auth_token():
        if "X-Api-Auth-Token" in request.headers:
            token = Token.cache_get(request.headers["X-Api-Auth-Token"])
            if token is not None and not token.expired:
                token.prolongate()
                return token.user

        return None

    def set_current_user(self):
        if ctx.envtype == 'development':
            username = os.getenv("DEV_USER")
            if username is not None:
                g.user = User.get(username)
                if g is not None:
                    return
        g.user = self._get_user_from_authorization_header() or \
            self._get_user_from_x_api_auth_token() or \
            self._get_user_from_session()
        if self.require_auth:
            if g.user is None:
                raise AuthenticationError()