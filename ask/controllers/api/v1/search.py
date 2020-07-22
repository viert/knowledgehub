from flask import request
from glasskit.api import json_response, paginated, default_transform
from glasskit.errors import InputDataError

from ask.controllers import AuthController
from ask.search import search_posts_generic

search_ctrl = AuthController("search", __name__, require_auth=False)

SEARCH_FIELDS = (
    "_id",
    "body",
    "title",
    "type",
    "parent_id",
    "_score",
    "question_title",
)


@search_ctrl.route("/")
def search():
    query = request.values.get("q")
    if query is None:
        raise InputDataError("'q' param is missing")
    result = search_posts_generic(query)
    return json_response(paginated(result, transform=default_transform(SEARCH_FIELDS)))
