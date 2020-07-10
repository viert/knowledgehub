from typing import Union, Dict, Any
from pymongo import ASCENDING, DESCENDING
from flask import has_request_context

from glasskit.uorm.models.submodel import StorableSubmodel
from glasskit.uorm.models.fields import (StringField, ObjectIdField, DatetimeField,
                                         IntField, BoolField, ListField)
from glasskit.uorm.utils import save_required
from glasskit.uorm.db import ObjectsCursor
from glasskit.utils import now, get_user_from_app_context

from ask.errors import InvalidUser, InvalidParent, InvalidQuestion, InvalidTags, HasReferences
from ask.tasks import SyncTagsTask


class BasePost(StorableSubmodel):

    COLLECTION = "posts"

    author_id: ObjectIdField(required=True, rejected=True, index=True)
    body: StringField(required=True, min_length=10, max_length=65536)
    created_at: DatetimeField(required=True, rejected=True, default=now, index=-1)
    edited_at: DatetimeField(rejected=True, default=None)
    deleted_at: DatetimeField(rejected=True, default=None)
    edited_by_id: ObjectIdField(rejected=True, default=None)
    deleted_by_id: ObjectIdField(rejected=True, default=None)
    deleted: BoolField(required=True, rejected=True, default=False)
    points: IntField(required=True, rejected=True, default=0, index=-1)

    @property
    def author(self) -> Union['User', None]:
        return User.find_one({"_id": self.author_id})

    @property
    def edited_by(self) -> Union['User', None]:
        if self.edited_by_id is None:
            return None
        return User.find_one({"_id": self.edited_by_id})

    @property
    def deleted_by(self) -> Union['User', None]:
        if self.deleted_by_id is None:
            return None
        return User.find_one({"_id": self.deleted_by_id})

    @property
    def my_vote(self) -> int:
        if not has_request_context():
            return 0
        u = get_user_from_app_context()
        if u is None:
            return 0
        v = Vote.find_one({"post_id": self._id, "user_id": u._id})
        return v.value if v is not None else 0

    @property
    def votes(self) -> ObjectsCursor:
        return Vote.find({"post_id": self._id})

    @property
    def update_allowed(self) -> bool:
        user: User = get_user_from_app_context()
        return self.author_id == user._id or user.moderator

    @property
    def delete_allowed(self) -> bool:
        user: User = get_user_from_app_context()
        return self.author_id == user._id or user.moderator

    @save_required
    def create_comment(self, attrs):
        attrs["parent_id"] = self._id
        return Comment(attrs)

    def update_by(self, user: 'User', attrs, skip_callback=False, invalidate_cache=True) -> None:
        self.edited_by_id = user._id
        self.edited_at = now()
        self.update(attrs, skip_callback=skip_callback, invalidate_cache=invalidate_cache)

    def delete_by(self, user: 'User', skip_callback=False, invalidate_cache=True) -> None:
        self.deleted_by_id = user._id
        self.deleted_at = now()
        self.deleted = True
        self.save(skip_callback=skip_callback, invalidate_cache=invalidate_cache)

    def _before_save(self) -> None:
        if self.author is None:
            raise InvalidUser("author_id is invalid or author not found")
        if self.edited_by_id is not None and self.edited_by is None:
            raise InvalidUser("edited_by_id is invalid or user not found")
        if self.deleted_by_id is not None and self.deleted_by is None:
            raise InvalidUser("deleted_by_id is invalid or user not found")

    def api_dict(self, fields=None, include_restricted=False) -> Dict[str, Any]:
        d = self.to_dict(fields, include_restricted)
        if self.deleted:
            d["body"] = None
        if "submodel" in d:
            del d["submodel"]
        return d

    def recalculate_points(self) -> None:
        positive = Vote.find({"post_id": self._id, "value": 1}).count()
        negative = Vote.find({"post_id": self._id, "value": -1}).count()
        self.points = positive - negative
        self.save(skip_callback=True)


class Question(BasePost):

    title: StringField(required=True, min_length=5, max_length=120)
    tags: ListField(required=True, min_length=1, default=list)
    views_count: IntField(required=True, default=0, rejected=True, index=True)
    answers_count: IntField(required=True, default=0, rejected=True, index=True)
    has_accepted_answer: BoolField(required=True, default=False, rejected=True, index=True)
    last_activity_at: DatetimeField(required=True, default=now, rejected=True, index=-1)
    closed: BoolField(required=True, default=False, rejected=True)

    SUBMODEL = "question"
    USE_INITIAL_STATE = False

    INDEXES = (
        [[("tags", 1), ("points", -1)], {}],
    )

    def setup_initial_state(self) -> Dict[str, Any]:
        # return {"tags": self.tags[:]}
        return {}

    @property
    def answers(self) -> ObjectsCursor:
        return Answer.find({"parent_id": self._id, "deleted": False}).sort([
            ("accepted", DESCENDING),
            ("points", DESCENDING),
        ])

    @property
    def comments(self) -> ObjectsCursor:
        return Comment.find({"parent_id": self._id}).sort("created_at", ASCENDING)

    def update_answers_count(self) -> None:
        self.answers_count = self.answers.count()
        self.save(skip_callback=True)

    @save_required
    def create_answer(self, attrs):
        attrs["parent_id"] = self._id
        return Answer(attrs)

    @save_required
    def sync_tags(self) -> None:
        """
        May be heavy, do not use from real-time API code
        """
        Tag.sync(self.tags)

    def _before_save(self) -> None:
        new_tags = set(self.tags)
        if len(self.tags) != len(new_tags):
            raise InvalidTags("tags must be unique")

        if self.is_new:
            self._tags_changed = new_tags
        else:
            old_tags = set(self._initial_state["tags"])
            if new_tags != old_tags:
                # all tags should be recalculated, including
                # removed ones
                self._tags_changed = new_tags.union(old_tags)
            else:
                self._tags_changed = set()

        if not self.is_new:
            self.update_last_activity()

    def _after_save(self, is_new) -> None:
        if self._tags_changed:
            task = SyncTagsTask.create(self.tags)
            task.publish()

    def _before_delete(self) -> None:
        """
        This should not be used by design, as questions should only
        be marked as deleted, not deleted from db.

        However this method will make sure that the question has no
        answers and/or comments attached to it
        """
        if self.comments.count() > 0:
            raise HasReferences("question have comments attached")
        if self.answers.count() > 0:
            raise HasReferences("question have answers attached")

        # at this point there's no not deleted comments or answers,
        # let's kill others (i.e. marked as deleted)
        Answer.destroy_many({"parent_id": self._id})
        Comment.destroy_many({"parent_id": self._id})

    def _after_delete(self) -> None:
        # tags should be recalculated
        task = SyncTagsTask.create(self.tags)
        task.publish()

    def update_last_activity(self) -> None:
        self.last_activity_at = now()

    def set_accepted_answer(self, answer) -> None:
        if answer is not None and answer.parent_id != self._id:
            raise InvalidParent("can't accept answer to different question")

        # reset current accepted answer
        for current in self.answers:
            if current.accepted:
                current.accepted = False
                current.save(skip_callback=True)

        if answer is not None:
            answer.accepted = True
            answer.save(skip_callback=True)
            self.has_accepted_answer = True
        else:
            self.has_accepted_answer = False

        self.update_last_activity()
        self.save(skip_callback=True)

    def everything(self, user: Union['User', None] = None) -> Dict[str, Any]:
        if user is None:
            user = get_user_from_app_context()
        user_id = user._id if user else None

        qa_pipeline = [
            {"$match": {"$or": [
                {"_id": self._id},
                {"parent_id": self._id, "submodel": "answer"},
            ]}},
            {"$lookup": {
                "from": "votes",
                "let": {"post_id": "$_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$and": [
                                {"$eq": ["$post_id", "$$post_id"]},
                                {"$eq": ["$user_id", user_id]}
                            ]
                        }
                    }},
                    {"$project": {
                        "_id": 0,
                        "value": 1
                    }}
                ],
                "as": "votes",
            }}
        ]

        results = {
            "question": None,
            "answers": [],
            "comments": [],
            "authors": []
        }
        author_ids = set()
        doc_ids = []

        for doc in BasePost.aggregate(qa_pipeline):
            doc["my_vote"] = doc["votes"][0]["value"] if doc["votes"] else 0
            del doc["votes"]

            doc_ids.append(doc["_id"])
            if doc["submodel"] == "question":
                results["question"] = doc
            elif doc["submodel"] == "answer":
                results["answers"].append(doc)
            author_ids.add(doc["author_id"])

        c_pipeline = [
            {
                "$match": {"parent_id": {"$in": doc_ids}, "submodel": "comment"},
            },
            {
                "$lookup": {
                    "from": "votes",
                    "let": {"post_id": "$_id"},
                    "pipeline": [
                        {"$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$post_id", "$$post_id"]},
                                    {"$eq": ["$user_id", user_id]}
                                ]
                            }
                        }},
                        {"$project": {
                            "_id": 0,
                            "value": 1
                        }}
                    ],
                    "as": "votes",
                }
            }
        ]

        for doc in BasePost.aggregate(c_pipeline):
            doc["my_vote"] = doc["votes"][0]["value"] if doc["votes"] else 0
            del doc["votes"]
            results["comments"].append(doc)
            author_ids.add(doc["author_id"])

        results["authors"] = (User.find({"_id": {"$in": list(author_ids)}}))

        return results


class Answer(BasePost):

    SUBMODEL = "answer"

    accepted: BoolField(required=True, default=False, rejected=True)
    parent_id: ObjectIdField(required=True, rejected=True)

    INDEXES = (
        [[("parent_id", 1), ("accepted", 1), ("points", 1)], {}],
        [[("parent_id", 1), ("accepted", 1), ("created_at", 1)], {}],
        [[("parent_id", 1), ("deleted", 1)], {}],
    )

    @property
    def question(self) -> Question:
        return Question.find_one({"_id": self.parent_id})

    @property
    def comments(self) -> ObjectsCursor:
        return Comment.find({"parent_id": self._id}).sort("created_at", ASCENDING)

    def _before_save(self) -> None:
        super()._before_save()
        if self.question is None:
            raise InvalidQuestion("parent_id is invalid or question not found")

    def _after_save(self, is_new) -> None:
        q = self.question
        q.update_last_activity()
        q.update_answers_count()


class Comment(BasePost):

    SUBMODEL = "comment"

    parent_id: ObjectIdField(required=True, rejected=True)

    INDEXES = (
        [[("parent_id", 1), ("created_at", 1)], {}],
    )

    @property
    def parent(self) -> Union[Answer, Question]:
        return BasePost.find_one({"_id": self.parent_id})

    @property
    def question(self) -> Question:
        q = self.parent
        if isinstance(q, Answer):
            q = q.question
        return q

    def _before_save(self) -> None:
        p = self.parent
        if p is None:
            raise InvalidParent("invalid parent_id or parent not found")
        if isinstance(p, Comment):
            raise InvalidParent("can not attach comment to another comment")
        q = self.question
        q.update_last_activity()
        q.save(skip_callback=True)


BasePost.register_submodel(Question.SUBMODEL, Question)
BasePost.register_submodel(Comment.SUBMODEL, Comment)
BasePost.register_submodel(Answer.SUBMODEL, Answer)

from .user import User
from .vote import Vote
from .tag import Tag
