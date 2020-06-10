from uengine.models.storable_model import StorableModel
from uengine.models.abstract_model import DoNotSave
from uengine.utils import now

from ask.errors import InvalidVote, InvalidUser, InvalidPost


class Vote(StorableModel):

    COLLECTION = "votes"

    FIELDS = (
        "_id",
        "user_id",
        "post_id",
        "value",
        "added_at",
    )

    REQUIRED_FIELDS = (
        "user_id",
        "post_id",
        "value",
    )

    VALIDATION_TYPES = {
        "value": int,
    }

    DEFAULTS = {
        "value": 1,
        "added_at": now
    }

    INDEXES = (
        ["post_id", "user_id", {"unique": True}],
    )

    @property
    def post(self):
        from .post import BasePost
        return BasePost.find_one({"_id": self.post_id})

    @property
    def user(self):
        from .user import User
        return User.find_one({"_id": self.user_id})

    def _before_save(self):
        if self.value == 0:
            if not self.is_new:
                self.destroy()
            raise DoNotSave()

        if abs(self.value) != 1:
            raise InvalidVote("vote value can be either 1 or -1")

        if self.post is None:
            raise InvalidPost("post_id is invalid or post not found")
        if self.user is None:
            raise InvalidUser("user_id is invalid or user not found")

    @classmethod
    def vote(cls, post_id, user_id, value):
        from .post import BasePost

        v = cls.find_one({"post_id": post_id, "user_id": user_id})
        if v:
            if value != v.value:
                v.value = value
                v.added_at = now()
                v.save()
            else:
                return v
        else:
            v = cls(post_id=post_id, user_id=user_id, value=value)
            v.save()

        p = BasePost.find_one({"_id": post_id})
        p.recalculate_points()

        if p.submodel != "question":
            p = p.question

        p.update_last_activity()
        p.save(skip_callback=True)

        return v
