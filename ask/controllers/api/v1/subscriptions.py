from flask import request
from glasskit.api import json_response, json_body_required
from glasskit.errors import InputDataError
from glasskit.utils import get_user_from_app_context, resolve_id

from ask.controllers import AuthController
from ask.models import User

subs_ctrl = AuthController("subscriptions", __name__, require_auth=True)

TAG_SUBSCRIPTION_FIELDS = (
    "_id",
    "tags",
    "user_id",
)

USER_SUBSCRIPTION_FIELDS = (
    "_id",
    "subs_user_ids",
    "user_id",
)


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


@subs_ctrl.route("/users", methods=["POST"])
@json_body_required
def users_subscribe():
    user: User = get_user_from_app_context()
    user_ids = request.json.get("user_ids")
    if user_ids is None:
        raise InputDataError("user_ids field is mandatory")
    user_ids = [resolve_id(user_id) for user_id in user_ids]

    us = user.user_subscription
    us.subs_user_ids = user_ids
    us.save()

    json_response({"data": us.to_dict(fields=USER_SUBSCRIPTION_FIELDS)})
