from flask import session, request, redirect
from uengine import ctx
from uengine.utils import get_user_from_app_context
from uengine.api import json_response, json_body_required
from uengine.errors import InputDataError

from ask.controllers.auth_controller import AuthController, AuthenticationError
from ask.idconnect.provider import BaseProvider
from ask.models import User

account_ctrl = AuthController("account", __name__, require_auth=False)

ACCOUNT_FIELDS = (
    "_id",
    "username",
    "first_name",
    "last_name",
    "ext_id",
)


@account_ctrl.route("/me")
def me():
    user = get_user_from_app_context()
    if user is None:
        raise AuthenticationError()
    return json_response({
        "data": user.to_dict(ACCOUNT_FIELDS),
        "providers": BaseProvider.list_provider_info()
    })


@account_ctrl.route("/oauthinfo", methods=["GET"])
def oauth():
    return json_response({"providers": BaseProvider.list_provider_info()})


@account_ctrl.route("/oauth_callback", methods=["GET"])
def oauth_callback():
    code = request.values.get("code")
    state = request.values.get("state")
    if not code:
        raise AuthenticationError("no code from provider")
    if not state:
        raise AuthenticationError("no state from provider")
    provider = BaseProvider.get_provider(state)

    token = provider.acquire_token(code)
    user_data = provider.get_user_data(token)

    user = User.find_one({"ext_id": user_data["ext_id"]})
    if not user:
        user = User(**user_data)
        user.save()
    session["user_id"] = user._id
    session.modified = True

    return redirect(ctx.cfg["base_uri"])


@account_ctrl.route("/logout", methods=["POST"])
def logout():
    session["user_id"] = None
    session.modified = True
    raise AuthenticationError()
