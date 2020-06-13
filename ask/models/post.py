from pymongo import ASCENDING, DESCENDING
from flask import has_request_context

from uengine.models.submodel import StorableSubmodel
from uengine.models.abstract_model import save_required
from uengine.utils import now, get_user_from_app_context

from ask.errors import InvalidUser, InvalidParent, InvalidQuestion, InvalidTags, HasReferences
from ask.tasks import SyncTagsTask


class BasePost(StorableSubmodel):

    COLLECTION = "posts"

    FIELDS = (
        "_id",
        "author_id",
        "created_at",
        "edited_at",
        "edited_by_id",
        "body",
        "deleted",
        "deleted_at",
        "deleted_by_id",
        "points",
    )

    REJECTED_FIELDS = (
        "author_id",
        "created_at",
        "edited_at",
        "edited_by_id",
        "deleted",
        "deleted_at",
        "deleted_by_id",
        "points",
    )

    DEFAULTS = {
        "created_at": now,
        "points": 0,
        "deleted": False,
    }

    REQUIRED_FIELDS = (
        "author_id",
        "body",
    )

    INDEXES = (
        "author_id",
        "created_at",
        "points",
    )

    @property
    def author(self):
        from .user import User
        return User.find_one({"_id": self.author_id})

    @property
    def edited_by(self):
        from .user import User
        return User.find_one({"_id": self.edited_by_id})

    @property
    def deleted_by(self):
        from .user import User
        return User.find_one({"_id": self.deleted_by_id})

    @property
    def my_vote(self):
        from .vote import Vote
        if not has_request_context():
            return 0
        u = get_user_from_app_context()
        if u is None:
            return 0
        v = Vote.find_one({"post_id": self._id, "user_id": u._id})
        return v.value if v is not None else 0

    @property
    def votes(self):
        from .vote import Vote
        return Vote.find({"post_id": self._id})

    @property
    def update_allowed(self):
        user = get_user_from_app_context()
        return self.author_id == user._id or user.moderator

    @property
    def delete_allowed(self):
        user = get_user_from_app_context()
        return self.author_id == user._id or user.moderator

    @save_required
    def create_comment(self, **kwargs):
        return Comment(**kwargs, parent_id=self._id)

    def update_by(self, user, data, skip_callback=False, invalidate_cache=True):
        self.edited_by_id = user._id
        self.edited_at = now()
        self.update(data, skip_callback=skip_callback, invalidate_cache=invalidate_cache)

    def delete_by(self, user, skip_callback=False, invalidate_cache=True):
        self.deleted_by_id = user._id
        self.deleted_at = now()
        self.deleted = True
        self.save(skip_callback=skip_callback, invalidate_cache=invalidate_cache)

    def _before_save(self):
        if self.author_id is not None and self.author is None:
            raise InvalidUser("author_id is invalid or author not found")
        if self.edited_by_id is not None and self.edited_by is None:
            raise InvalidUser("edited_by_id is invalid or user not found")
        if self.deleted_by_id is not None and self.deleted_by is None:
            raise InvalidUser("deleted_by_id is invalid or user not found")

    def api_dict(self, fields=None, include_restricted=False):
        d = self.to_dict(fields, include_restricted)
        if self.deleted:
            d["body"] = None
        del d["submodel"]
        return d

    def recalculate_points(self):
        from .vote import Vote
        positive = Vote.find({"post_id": self._id, "value": 1}).count()
        negative = Vote.find({"post_id": self._id, "value": -1}).count()
        self.points = positive - negative
        self.save(skip_callback=True)


class Question(BasePost):

    SUBMODEL = "question"

    USE_INITIAL_STATE = True

    FIELDS = (
        "title",
        "views_count",
        "tags",
        "answers_count",
        "has_accepted_answer",
        "last_activity_at",
        "closed",
    )

    DEFAULTS = {
        "views_count": 0,
        "tags": list,
        "answers_count": 0,
        "has_accepted_answer": False,
        "last_activity_at": now,
        "closed": False,
    }

    REQUIRED_FIELDS = (
        "title",
    )

    REJECTED_FIELDS = (
        "closed",
        "answers_count",
        "views_count",
        "has_accepted_answer",
        "last_activity_at",
    )

    VALIDATION_TYPES = {
        "tags": list,
        "has_accepted_answer": bool,
        "closed": bool,
    }

    INDEXES = (
        ["tags", "-points"],
        "views_count",
        "answers_count",
        "has_accepted_answer",
        "last_activity_at",
    )

    def setup_initial_state(self):
        setattr(self, "_initial_state", {"tags": self.tags[:]})

    @property
    def answers(self):
        return Answer.find({"parent_id": self._id, "deleted": False}).sort([
            ("accepted", DESCENDING),
            ("points", DESCENDING),
        ])

    @property
    def comments(self):
        return Comment.find({"parent_id": self._id}).sort("created_at", ASCENDING)

    def update_answers_count(self):
        self.answers_count = self.answers.count()
        self.save(skip_callback=True)

    @save_required
    def create_answer(self, **kwargs):
        return Answer(**kwargs, parent_id=self._id)

    @save_required
    def sync_tags(self):
        """
        May be heavy
        """
        from .tag import Tag
        Tag.sync(self.tags)

    def _before_save(self):
        new_tags = set(self.tags)
        if len(self.tags) != len(new_tags):
            raise InvalidTags("tags must be unique")

        if len(self.tags) == 0:
            raise InvalidTags("questino must have at least one tag")

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

    def _after_save(self, is_new):
        if self._tags_changed:
            task = SyncTagsTask.create(self.tags)
            task.publish()

    def _before_delete(self):
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

    def _after_delete(self):
        # tags should be recalculated
        task = SyncTagsTask.create(self.tags)
        task.publish()

    def update_last_activity(self):
        self.last_activity_at = now()

    def set_accepted_answer(self, answer):
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

    def everything(self, user=None):
        from .user import User
        if user == None:
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
            {"$match":
                {"parent_id": {"$in": doc_ids}, "submodel": "comment"},
            },
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

        for doc in BasePost.aggregate(c_pipeline):
            doc["my_vote"] = doc["votes"][0]["value"] if doc["votes"] else 0
            del doc["votes"]
            results["comments"].append(doc)
            author_ids.add(doc["author_id"])

        results["authors"] = (User.find({"_id": {"$in": list(author_ids)}}))

        return results


class Answer(BasePost):

    SUBMODEL = "answer"

    FIELDS = (
        "accepted",
        "parent_id",
    )

    REQUIRED_FIELDS = (
        "parent_id",
    )

    REJECTED_FIELDS = (
        "accepted",
        "parent_id",
    )

    DEFAULTS = {
        "accepted": False,
    }

    INDEXES = (
        ["parent_id", "accepted", "points"],
        ["parent_id", "accepted", "created_at"],
        ["parent_id", "deleted"],
    )

    @property
    def question(self):
        return Question.find_one({"_id": self.parent_id})

    @property
    def comments(self):
        return Comment.find({"parent_id": self._id}).sort("created_at", ASCENDING)

    def _before_save(self):
        super()._before_save()
        if self.question is None:
            raise InvalidQuestion("parent_id is invalid or question not found")

    def _after_save(self, is_new):
        q = self.question
        q.update_last_activity()
        q.update_answers_count()


class Comment(BasePost):

    SUBMODEL = "comment"

    FIELDS = (
        "parent_id",
    )

    REQUIRED_FIELDS = (
        "parent_id",
    )

    REJECTED_FIELDS = (
        "parent_id",
    )

    INDEXES = (
        ["parent_id", "created_at"],
    )

    @property
    def parent(self):
        return BasePost.find_one({"_id": self.parent_id})

    @property
    def question(self):
        q = self.parent
        if isinstance(q, Answer):
            q = q.question
        return q

    def _before_save(self):
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
