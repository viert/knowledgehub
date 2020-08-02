from flask import request
from glasskit.api import json_response, json_body_required
from glasskit.utils import get_user_from_app_context
from glasskit.errors import ApiError
from ask.controllers import AuthController
from ask.api import auth_required
from ask.models import Tag, User


tags_ctrl = AuthController("tags", __name__, require_auth=False)


@tags_ctrl.route("/<tagname>")
def show(tagname):
    tag = Tag.get(tagname, "tag not found")
    return json_response({"data": tag.to_dict()})


@tags_ctrl.route("/<tagname>/subscribe", methods=["POST"])
@auth_required
def subscribe(tagname):
    Tag.get(tagname, "tag not found")
    user: User = get_user_from_app_context()
    user.subscribe_to_tag(tagname)
    return json_response({"data": user.tag_subscription.to_dict()})


@tags_ctrl.route("/<tagname>/unsubscribe", methods=["POST"])
@auth_required
def unsubscribe(tagname):
    Tag.get(tagname, "tag not found")
    user: User = get_user_from_app_context()
    user.unsubscribe_from_tag(tagname)
    return json_response({"data": user.tag_subscription.to_dict()})


@tags_ctrl.route("/", methods=["POST"])
@auth_required
@json_body_required
def replace_subscription():
    if "tags" not in request.json:
        raise ApiError("tags field is mandatory")
    user: User = get_user_from_app_context()
    user.replace_tags(request.json["tags"])
    return json_response({"data": user.tag_subscription.to_dict()})
