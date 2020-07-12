from flask import request
from glasskit.utils import resolve_id
from glasskit.api import json_response
from ask.controllers import AuthController
from ask.models import User

users_ctrl = AuthController("users", __name__, require_auth=False)

USER_FIELDS = (
    "_id",
    "first_name",
    "last_name",
    "username",
    "ext_id",
)


@users_ctrl.route("/list/<ids>")
def users(ids):
    ids = ids.split(",")
    ids = [resolve_id(id_) for id_ in ids]
    items = User.find({
        "$or": [
            {"_id": {"$in": ids}},
            {"username": {"$in": ids}},
        ]
    })
    items = [user.to_dict(USER_FIELDS) for user in items]
    return {"data": items}


@users_ctrl.route("/suggest")
def suggest():
    import re
    query = {}
    prefix = request.values.get("prefix")
    if prefix:
        try:
            prefix = re.compile("^" + prefix)
            query = {"$or": [
                {"username": prefix},
                {"first_name": prefix},
                {"last_name": prefix},
            ]}
        except re.error:
            pass
    users = User.find(query).sort("username", 1).limit(10)
    users = [user.to_dict(fields=["username", "first_name", "last_name"]) for user in users]
    return json_response({"data": users})
