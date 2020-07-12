from glasskit.uorm.db import ObjectsCursor
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import ListField, ObjectIdField


class UserSubscription(StorableModel):

    user_id: ObjectIdField(required=True, rejected=True, index=True)
    subs_user_ids: ListField(required=True, rejected=True, index=True, default=list)

    @property
    def user(self) -> 'User':
        return User.find_one({"_id": self.user_id})

    @property
    def subscribed_to(self) -> ObjectsCursor:
        return User.find({"_id": {"$in": self.subs_user_ids}})


from .user import User
