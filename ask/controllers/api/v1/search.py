from bson import ObjectId
from typing import Union
from flask import request
from glasskit.api import json_response, paginated, default_transform
from glasskit.errors import InputDataError

from ask.controllers import AuthController
from ask.search import search_posts_generic
from ask.models import Answer, Question, User
from ask.unmark import unmark
from ask.utils import cut

search_ctrl = AuthController("search", __name__, require_auth=False)

SEARCH_FIELDS = (
    "_id",
    "body",
    "title",
    "type",
    "parent_id",
    "_score",
    "created_at",
    "tags",
    "question_title",
    "answers_count",
    "points",
    "author_id",
)


def transform(item: Union[Question, Answer]):
    doc = item.to_dict(SEARCH_FIELDS)
    doc["body"] = cut(unmark(doc["body"]))
    return doc


@search_ctrl.route("/")
def search():
    query = request.values.get("q")
    if query is None:
        raise InputDataError("'q' param is missing")
    posts = paginated(search_posts_generic(query), transform=transform)
    author_ids = {ObjectId(x["author_id"]) for x in posts["data"]}
    authors = User.find({"_id": {"$in": list(author_ids)}}).all()

    return json_response({
        "results": posts,
        "authors": {
            "data": authors
        }
    })
