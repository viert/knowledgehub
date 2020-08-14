from glasskit.uorm.db import ObjectsCursor
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import ListField, ObjectIdField
from glasskit.errors import InputDataError


class UserSubscription(StorableModel):

    USE_INITIAL_STATE = True

    user_id: ObjectIdField(required=True, rejected=True, index=True)
    subs_user_ids: ListField(required=True, rejected=True, index=True, default=list)

    def setup_initial_state(self):
        return {"subs_user_ids": self.subs_user_ids[:]}

    @property
    def user(self) -> 'User':
        return User.find_one({"_id": self.user_id})

    @property
    def subscribed_to(self) -> ObjectsCursor:
        return User.find({"_id": {"$in": self.subs_user_ids}})

    def _before_save(self):
        if self.user is None:
            raise InputDataError("user_id is invalid or user not found")
        for user_id in self.subs_user_ids:
            u = User.find_one({"_id": user_id})
            if u is None:
                raise InputDataError(f"subscription user_id {user_id} is invalid or user not found")


from .user import User
