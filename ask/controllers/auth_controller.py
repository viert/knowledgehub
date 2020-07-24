import os
from typing import Union
from flask import session, request
from glasskit import ctx
from glasskit.controller import Controller

from ask.models import Token, User
from ask.errors import AuthenticationError


class AuthController(Controller):

    auth_error = AuthenticationError

    @staticmethod
    def _get_user_from_session() -> Union[User, None]:
        user_id = session.get("user_id")
        if user_id:
            user = User.get(user_id)
            return user
        return None

    @staticmethod
    def _get_user_from_x_api_auth_token() -> Union[User, None]:
        if "X-Api-Auth-Token" in request.headers:
            token = Token.cache_get(request.headers["X-Api-Auth-Token"])
            if token is not None and not token.expired:
                token.prolongate()
                return token.user
        return None

    def get_current_user(self) -> Union[User, None]:
        if ctx.envtype == 'development':
            username = os.getenv("DEV_USER")
            if username is not None:
                return User.get(username)
        user = self._get_user_from_x_api_auth_token() or self._get_user_from_session()
        return user
