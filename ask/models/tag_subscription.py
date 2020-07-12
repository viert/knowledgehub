from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import ObjectIdField, ListField
from glasskit.errors import InputDataError
from ask.errors import InvalidTags


class TagSubscription(StorableModel):

    tags: ListField(required=True, default=list, index=True)
    user_id: ObjectIdField(required=True, unique=True)  # unique means one-to-one relation

    @property
    def user(self) -> 'User':
        return User.find_one({"_id": self.user_id})

    def _before_save(self):
        if self.user is None:
            raise InputDataError("user_id is invalid or user not found")
        if len(self.tags) != len(set(self.tags)):
            raise InvalidTags("tag list must be unique")


from .user import User
