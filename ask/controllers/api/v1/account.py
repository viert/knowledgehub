from flask import session, request, redirect
from glasskit import ctx
from glasskit.utils import get_user_from_app_context
from glasskit.api import json_response, json_body_required

from ask.api import auth_required
from ask.controllers import AuthController
from ask.idconnect.provider import BaseProvider
from ask.models import User
from ask.errors import AuthenticationError

account_ctrl = AuthController("account", __name__, require_auth=False)

ACCOUNT_FIELDS = (
    "_id",
    "username",
    "first_name",
    "last_name",
    "ext_id",
    "tag_subscription",
    "user_subscription",
    "avatar_url",
)

ACCOUNT_RESTRICTED_FIELDS = (
    "moderator",
    "email",
    "telegram_id",
    "icq_id",
    "notify_by_email",
    "notify_by_telegram",
    "notify_by_icq",
)


def account_dict(user):
    data = user.to_dict(ACCOUNT_FIELDS)
    for field in ACCOUNT_RESTRICTED_FIELDS:
        data[field] = getattr(user, field)
    return data


@account_ctrl.route("/me", methods=["GET"])
@auth_required
def me():
    user = get_user_from_app_context()
    return json_response({
        "data": account_dict(user),
        "providers": BaseProvider.list_provider_info()
    })


@account_ctrl.route("/me", methods=["PATCH"])
@auth_required
@json_body_required
def update_settings():
    user: User = get_user_from_app_context()
    user.update(request.json)
    return json_response({
        "data": account_dict(user),
    })


@account_ctrl.route("/oauth_info", methods=["GET"])
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

    tokens = state.split(":")
    if len(tokens) != 2:
        raise AuthenticationError("invalid state from provider. expected <provider>:<origin>")

    provider_name, origin = tokens

    provider = BaseProvider.get_provider(provider_name)
    token = provider.acquire_token(code)
    user_data = provider.get_user_data(token)

    user = User.find_one({"ext_id": user_data["ext_id"]})
    if not user:
        user = User(user_data)
        user.fixup_username()
        user.save()
    session["user_id"] = user._id
    session.modified = True

    path = ctx.cfg.get("base_uri", "http://localhost:8080/")
    return redirect(f"{path}#{origin}")


@account_ctrl.route("/logout", methods=["POST"])
def logout():
    session["user_id"] = None
    session.modified = True
    raise AuthenticationError()
