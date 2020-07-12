from glasskit.api import json_response
from ask.controllers import AuthController
from ask.models import Tag


tags_ctrl = AuthController("tags", __name__, require_auth=False)


@tags_ctrl.route("/<tagname>")
def show(tagname):
    tag = Tag.get(tagname, "tag not found")
    return json_response({"data": tag.to_dict()})
