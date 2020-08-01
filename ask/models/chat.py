from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import Field, ObjectIdField, StringField

from ask.errors import InvalidUser


class Chat(StorableModel):

    user_id: ObjectIdField(required=True, rejected=True, index=True)
    chat_id: Field(required=True, rejected=True)
    network_type: StringField(required=True, rejected=True, choices=["telegram", "icq"])

    INDEXES = (
        [[('chat_id', 1), ('chat_type', 1)], {}],
    )

    @property
    def user(self) -> 'User':
        return User.find_one({"_id": self.user_id})

    def _before_save(self) -> None:
        if self.user is None:
            raise InvalidUser("user_id is invalid or user not found")


from .user import User
