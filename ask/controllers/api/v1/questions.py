from pymongo import DESCENDING
from flask import request

from uengine.api import (json_response, paginated, default_transform,
                         json_body_required)
from uengine.utils import get_user_from_app_context, resolve_id
from uengine.errors import ApiError

from ask.controllers.auth_controller import AuthController
from ask.models import Question, Vote, User
from ask.api import auth_required

questions_ctrl = AuthController("questions", __name__, require_auth=False)


QUESTION_LIST_FIELDS = (
    "_id",
    "title",
    "author_id",
    "points",
    "created_at",
    "edited_at",
    "views_count",
    "tags",
    "answers_count",
    "has_accepted_answer",
    "last_activity_at",
    "closed",
)

QUESTION_FIELDS = (
    "_id",
    "title",
    "body",
    "author_id",
    "points",
    "my_vote",
    "created_at",
    "edited_at",
    "views_count",
    "tags",
    "answers_count",
    "has_accepted_answer",
    "last_activity_at",
    "closed",
)

ANSWER_FIELDS = (
    "_id",
    "body",
    "author_id",
    "question_id",
    "points",
    "my_vote",
    "created_at",
    "edited_at",
    "accepted",
)

SORT_MAP = {
    "rating": [
        ("points", DESCENDING), ("last_activity_at", DESCENDING)
    ],
    "date": [("created_at", DESCENDING)]
}


@questions_ctrl.route("/", methods=["GET"])
def index():
    if "sort" in request.values:
        sort = request.values["sort"]
    else:
        sort = "rating"

    sortExpr = SORT_MAP.get(sort)
    if sortExpr is None:
        raise ApiError(f"unknown sort operator \"{sort}\"")

    questions = Question.find({"deleted": False}).sort(sort)
    results = paginated(questions,
                        transform=default_transform(fields=QUESTION_LIST_FIELDS))
    author_ids = set()
    for q in results["data"]:
        author_ids.add(resolve_id(q["author_id"]))
    authors = User.find({"_id": {"$in": list(author_ids)}})
    return json_response({
        "questions": results,
        "authors": {"data": authors}
    })


@questions_ctrl.route("/<question_id>", methods=["GET"])
def show(question_id):
    q = Question.get(question_id, "question not found")
    return json_response({"data": q.everything()})


@questions_ctrl.route("/<question_id>/vote", methods=["POST"])
@json_body_required
@auth_required
def vote_question(question_id):
    q = Question.get(question_id, "question not found")
    u = get_user_from_app_context()
    attrs = request.json

    if "value" not in attrs:
        raise ApiError("value field is mandatory")

    Vote.vote(q._id, u._id, attrs["value"])
    q.reload()
    return json_response({"data": q.api_dict(fields=QUESTION_FIELDS)})


@questions_ctrl.route("/<question_id>/answers", methods=["POST"])
@json_body_required
@auth_required
def create_answer(question_id):
    q = Question.get(question_id, "question not found")
    u = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body field is mandatory")

    a = q.create_answer(author_id=u._id, body=attrs["body"])
    a.save()

    return json_response({"data": a.api_dict()})
