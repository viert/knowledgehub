from pymongo import DESCENDING
from flask import request

from glasskit.api import (json_response, paginated, default_transform,
                          json_body_required)
from glasskit.utils import get_user_from_app_context, resolve_id
from glasskit.errors import ApiError, NotFound, Forbidden

from ask.controllers import AuthController
from ask.models import Question, Answer, Comment, Vote, User
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
    "parent_id",
    "points",
    "my_vote",
    "created_at",
    "edited_at",
    "accepted",
)

COMMENT_FIELDS = (
    "_id",
    "body",
    "author_id",
    "parent_id",
    "points",
    "my_vote",
    "created_at",
    "edited_at",
)

SORT_MAP = {
    "rating": [
        ("points", DESCENDING), ("last_activity_at", DESCENDING)
    ],
    "date": [("created_at", DESCENDING)]
}


def update_post(post):
    if not post.update_allowed:
        raise Forbidden("you can't edit this post")
    attrs = request.json
    user = get_user_from_app_context()
    post.update_by(user, attrs)


def delete_post(post):
    if not post.delete_allowed:
        raise Forbidden("you can't delete this post")
    user = get_user_from_app_context()
    post.delete_by(user)


@questions_ctrl.route("/", methods=["GET"])
def index():
    # TODO: mine=true param
    if "_sort" in request.values:
        srt = request.values["_sort"]
    else:
        srt = "rating"

    sortExpr = SORT_MAP.get(srt)
    if sortExpr is None:
        raise ApiError(f"unknown sort operator \"{srt}\"")

    questions = Question.find({"deleted": False}).sort(sortExpr)
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


@questions_ctrl.route("/<question_id>", methods=["PATCH"])
@json_body_required
@auth_required
def update(question_id):
    q = Question.get(question_id, "question not found")
    update_post(q)
    return json_response({"data": q.api_dict(QUESTION_FIELDS)})


@questions_ctrl.route("/<question_id>", methods=["DELETE"])
@auth_required
def delete(question_id):
    q = Question.get(question_id, "question not found")
    delete_post(q)
    return json_response({"data": q.api_dict(QUESTION_FIELDS)})


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


@questions_ctrl.route("/", methods=["POST"])
@json_body_required
@auth_required
def create():
    user = get_user_from_app_context()
    attrs = request.json
    q = Question(**attrs, author_id=user._id)
    q.save()
    return json_response({"data": q.api_dict(fields=QUESTION_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/", methods=["POST"])
@json_body_required
@auth_required
def create_answer(question_id):
    q = Question.get(question_id, "question not found")
    u = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body is missing")

    a = q.create_answer(author_id=u._id, body=attrs["body"])
    a.save()

    return json_response({"data": a.api_dict()})


@questions_ctrl.route("/<question_id>/answers/<answer_id>", methods=["PATCH"])
@json_body_required
@auth_required
def update_answer(question_id, answer_id):
    a = Answer.get(answer_id, "answer not found")
    if a.parent_id != resolve_id(question_id):
        raise NotFound("answer not found")
    update_post(a)
    return json_response({"data": a.api_dict(ANSWER_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>", methods=["DELETE"])
@auth_required
def delete_answer(question_id, answer_id):
    a = Answer.get(answer_id, "answer not found")
    if a.parent_id != resolve_id(question_id):
        raise NotFound("answer not found")
    delete_post(a)
    return json_response({"data": a.api_dict(ANSWER_FIELDS)})


@questions_ctrl.route("/<question_id>/comments/", methods=["POST"])
@json_body_required
@auth_required
def create_comment(question_id):
    q = Question.get(question_id, "question not found")
    user = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body is missing")

    c = q.create_comment(body=attrs["body"], author_id=user._id)
    c.save()
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/comments/<comment_id>", methods=["PATCH"])
@json_body_required
@auth_required
def update_comment(question_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    if c.parent_id != resolve_id(question_id):
        raise NotFound("comment not found")
    update_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/comments/<comment_id>", methods=["PATCH"])
@auth_required
def delete_comment(question_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    if c.parent_id != resolve_id(question_id):
        raise NotFound("comment not found")
    delete_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/comments", methods=["POST"])
@json_body_required
@auth_required
def create_answer_comment(question_id, answer_id):
    a = Answer.get(answer_id, "answer not found")
    if a.parent_id != resolve_id(question_id):
        raise NotFound("answer not found")
    user = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body is missing")

    c = a.create_comment(body=attrs["body"], author_id=user._id)
    c.save()
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/comments/<comment_id>", methods=["PATCH"])
@json_body_required
@auth_required
def update_answer_comment(question_id, answer_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    a = Answer.get(answer_id, "comment not found")
    q = Question.get(question_id, "comment not found")
    if a.parent_id != q._id or c.parent_id != a._id:
        raise NotFound("comment not found")
    update_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/comments/<comment_id>", methods=["DELETE"])
@auth_required
def delete_answer_comment(question_id, answer_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    a = Answer.get(answer_id, "comment not found")
    q = Question.get(question_id, "comment not found")
    if a.parent_id != q._id or c.parent_id != a._id:
        raise NotFound("comment not found")
    delete_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})
