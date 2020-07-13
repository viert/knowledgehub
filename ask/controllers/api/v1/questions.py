from pymongo import DESCENDING
from flask import request

from glasskit.api import (json_response, paginated, default_transform,
                          json_body_required, get_boolean_request_param)
from glasskit.utils import get_user_from_app_context, resolve_id
from glasskit.errors import ApiError, NotFound, Forbidden

from ask.controllers import AuthController
from ask.models import Question, Answer, Comment, Vote, User
from ask.errors import NotAccepted
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


def restore_post(post):
    if not post.restore_allowed:
        raise Forbidden("you can't restore this post")
    post.restore()


@questions_ctrl.route("/", methods=["GET"])
def index():
    if "_sort" in request.values:
        srt = request.values["_sort"]
    else:
        srt = "rating"

    sortExpr = SORT_MAP.get(srt)
    if sortExpr is None:
        raise ApiError(f"unknown sort operator \"{srt}\"")

    query = {"deleted": False}
    if get_boolean_request_param("_mine"):
        u: User = get_user_from_app_context()
        if u:
            query["author_id"] = u._id

    questions = Question.find(query).sort(sortExpr)
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


@questions_ctrl.route("/<question_id>/restore", methods=["POST"])
@auth_required
def restore(question_id):
    q = Question.get(question_id, "question not found")
    restore_post(q)
    return json_response({"data": q.api_dict(QUESTION_FIELDS)})


@questions_ctrl.route("/<question_id>/vote", methods=["POST"])
@json_body_required
@auth_required
def vote_question(question_id):
    q: Question = Question.get(question_id, "question not found")
    u: User = get_user_from_app_context()
    if q.author_id == u._id:
        raise Forbidden("you can't vote for your own question")

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
    user: User = get_user_from_app_context()
    attrs = request.json
    attrs["author_id"] = user._id
    q = Question(attrs)
    q.save()
    return json_response({"data": q.api_dict(fields=QUESTION_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/", methods=["POST"])
@json_body_required
@auth_required
def create_answer(question_id):
    q = Question.get(question_id, "question not found")
    user: User = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body is missing")

    a = q.create_answer({"author_id": user._id, "body": attrs["body"]})
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


@questions_ctrl.route("/<question_id>/answers/<answer_id>/restore", methods=["POST"])
@auth_required
def restore_answer(question_id, answer_id):
    a = Answer.get(answer_id, "answer not found")
    if a.parent_id != resolve_id(question_id):
        raise NotFound("answer not found")
    restore_post(a)
    return json_response({"data": a.api_dict(ANSWER_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/vote", methods=["POST"])
@json_body_required
@auth_required
def vote_answer(question_id, answer_id):
    a = Answer.get(answer_id, "answer not found")
    if a.parent_id != resolve_id(question_id):
        raise NotFound("answer not found")
    u: User = get_user_from_app_context()
    if a.author_id == u._id:
        raise Forbidden("you can't vote for your own answers")

    attrs = request.json

    if "value" not in attrs:
        raise ApiError("value field is mandatory")

    Vote.vote(a._id, u._id, attrs["value"])
    a.reload()
    return json_response({"data": a.api_dict(fields=ANSWER_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/accept", methods=["POST"])
@auth_required
def accept_answer(question_id, answer_id):
    u: User = get_user_from_app_context()
    q: Question = Question.get(question_id, "answer not found")
    a: Answer = Answer.get(answer_id, "answer not found")
    if a.parent_id != q._id:
        raise NotFound("answer not found")
    if q.author_id != u._id:
        raise Forbidden("only question's author can accept answers")
    q.set_accepted_answer(a)
    return json_response({"data": a.api_dict(ANSWER_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/revoke", methods=["POST"])
@auth_required
def revoke_answer(question_id, answer_id):
    u: User = get_user_from_app_context()
    q: Question = Question.get(question_id, "answer not found")
    a: Answer = Answer.get(answer_id, "answer not found")
    if a.parent_id != q._id:
        raise NotFound("answer not found")
    if q.author_id != u._id:
        raise Forbidden("only question's author can revoke answers")
    if not a.accepted:
        raise NotAccepted("answer is not accepted so can't be revoked")
    q.set_accepted_answer(None)
    return json_response({"data": a.api_dict(ANSWER_FIELDS)})


@questions_ctrl.route("/<question_id>/comments/", methods=["POST"])
@json_body_required
@auth_required
def create_comment(question_id):
    q = Question.get(question_id, "question not found")
    user: User = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body is missing")

    c = q.create_comment({"body": attrs["body"], "author_id": user._id})
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


@questions_ctrl.route("/<question_id>/comments/<comment_id>", methods=["DELETE"])
@auth_required
def delete_comment(question_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    if c.parent_id != resolve_id(question_id):
        raise NotFound("comment not found")
    delete_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/comments/<comment_id>/restore", methods=["POST"])
@auth_required
def restore_comment(question_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    if c.parent_id != resolve_id(question_id):
        raise NotFound("comment not found")
    restore_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/comments/<comment_id>/vote", methods=["POST"])
@json_body_required
@auth_required
def vote_comment(question_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    if c.parent_id != resolve_id(question_id):
        raise NotFound("comment not found")
    u: User = get_user_from_app_context()
    if c.author_id == u._id:
        raise Forbidden("you can't vote for your own comments")

    attrs = request.json

    if "value" not in attrs:
        raise ApiError("value field is mandatory")

    Vote.vote(c._id, u._id, attrs["value"])
    c.reload()
    return json_response({"data": c.api_dict(fields=COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/comments/", methods=["POST"])
@json_body_required
@auth_required
def create_answer_comment(question_id, answer_id):
    a = Answer.get(answer_id, "answer not found")
    if a.parent_id != resolve_id(question_id):
        raise NotFound("answer not found")
    user: User = get_user_from_app_context()
    attrs = request.json

    if "body" not in attrs:
        raise ApiError("body is missing")

    c = a.create_comment({"body": attrs["body"], "author_id": user._id})
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


@questions_ctrl.route("/<question_id>/answers/<answer_id>/comments/<comment_id>/restore", methods=["POST"])
@auth_required
def restore_answer_comment(question_id, answer_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    a = Answer.get(answer_id, "comment not found")
    q = Question.get(question_id, "comment not found")
    if a.parent_id != q._id or c.parent_id != a._id:
        raise NotFound("comment not found")
    restore_post(c)
    return json_response({"data": c.api_dict(COMMENT_FIELDS)})


@questions_ctrl.route("/<question_id>/answers/<answer_id>/comments/<comment_id>/vote", methods=["POST"])
@json_body_required
@auth_required
def vote_answer_comment(question_id, answer_id, comment_id):
    c = Comment.get(comment_id, "comment not found")
    a = Answer.get(answer_id, "comment not found")
    q = Question.get(question_id, "comment not found")
    if a.parent_id != q._id or c.parent_id != a._id:
        raise NotFound("comment not found")
    u: User = get_user_from_app_context()
    if c.author_id == u._id:
        raise Forbidden("you can't vote for your own comments")

    attrs = request.json

    if "value" not in attrs:
        raise ApiError("value field is mandatory")

    Vote.vote(c._id, u._id, attrs["value"])
    c.reload()
    return json_response({"data": c.api_dict(fields=COMMENT_FIELDS)})
