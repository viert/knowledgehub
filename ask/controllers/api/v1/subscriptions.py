from flask import request
from glasskit.api import json_response, json_body_required
from glasskit.errors import InputDataError
from glasskit.utils import get_user_from_app_context, resolve_id

from ask.controllers import AuthController
from ask.models import User
from .users import USER_FIELDS

subs_ctrl = AuthController("subscriptions", __name__, require_auth=True)

TAG_SUBSCRIPTION_FIELDS = (
    "_id",
    "tags",
    "user_id",
)


@subs_ctrl.route("/tags", methods=["GET"])
def tag_subscription():
    user: User = get_user_from_app_context()
    ts = user.tag_subscription
    return json_response({"data": ts.tags})


@subs_ctrl.route("/users", methods=["GET"])
def users_subscription():
    user: User = get_user_from_app_context()
    us = user.user_subscription
    users = []
    for user in us.subscribed_to:
        users.append(user.to_dict(fields=USER_FIELDS))
    return json_response({"data": users})


@subs_ctrl.route("/tags", methods=["POST"])
@json_body_required
def tags_subscribe():
    user: User = get_user_from_app_context()
    tags = request.json.get("tags")
    if tags is None:
        raise InputDataError("tags field is mandatory")
    tags = list(set(tags))  # make sure tags are unique

    ts = user.tag_subscription
    ts.tags = tags
    ts.save()

    json_response({"data": ts.to_dict(fields=TAG_SUBSCRIPTION_FIELDS)})


@subs_ctrl.route("/users/:user_id/subscribe", methods=["POST"])
@json_body_required
def users_subscribe(user_id):
    current: User = get_user_from_app_context()
    user = User.get(user_id, "user not found")
    current.subscribe_to_user(user)
    return users_subscription()


@subs_ctrl.route("/users/:user_id/unsubscribe", methods=["POST"])
@json_body_required
def users_unsubscribe(user_id):
    current: User = get_user_from_app_context()
    user = User.get(user_id, "user not found")
    current.unsubscribe_from_user(user)
    return users_subscription()
