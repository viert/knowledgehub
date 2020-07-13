from bson import ObjectId
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import ObjectIdField, IntField, DatetimeField
from glasskit.uorm.errors import DoNotSave
from glasskit.errors import NotFound
from glasskit.utils import now

from ask.errors import InvalidVote, InvalidUser, InvalidPost


class Vote(StorableModel):

    COLLECTION = "votes"

    user_id: ObjectIdField(required=True, rejected=True)
    post_id: ObjectIdField(required=True, rejected=True)
    value: IntField(required=True, default=1, rejected=True)
    added_at: DatetimeField(required=True, default=now, rejected=True)

    INDEXES = (
        [[("post_id", 1), ("user_id", 1)], {"unique": True}],
    )

    @property
    def post(self) -> 'BasePost':
        return BasePost.find_one({"_id": self.post_id})

    @property
    def user(self) -> 'User':
        return User.find_one({"_id": self.user_id})

    def _before_save(self) -> None:
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
    def vote(cls, post_id: ObjectId, user_id: ObjectId, value: int) -> 'Vote':
        p = BasePost.find_one({"_id": post_id})
        if p is None:
            raise NotFound("post not found")

        if isinstance(p, Comment):
            if value < 0:
                raise InvalidVote("comments can only be up-voted")
        
        v = cls.find_one({"post_id": post_id, "user_id": user_id})
        if v:
            if value != v.value:
                v.value = value
                v.added_at = now()
                v.save()
            else:
                return v
        else:
            v = cls({
                "post_id": post_id,
                "user_id": user_id,
                "value": value
            })
            v.save()

        p.recalculate_points()

        if p.submodel != "question":
            p = p.question

        p.update_last_activity()
        p.save(skip_callback=True)

        return v


from .post import BasePost, Comment
from .user import User
