from uengine.utils import resolve_id
from ask.controllers.auth_controller import AuthController
from ask.models import User

users_ctrl = AuthController("users", __name__, require_auth=True)

USER_FIELDS = (
    "_id",
    "first_name",
    "last_name",
    "username",
    "ext_id",
)


@users_ctrl.route("/<ids>")
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
