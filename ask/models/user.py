from glasskit.utils import now
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import StringField, BoolField, DatetimeField


class User(StorableModel):

    ext_id: StringField(required=True, rejected=True, unique=True)
    username: StringField(required=True, unique=True)
    first_name: StringField(default="")
    last_name: StringField(default="")
    email: StringField(default="")
    avatar_url: StringField(default="")
    created_at: DatetimeField(required=True, rejected=True, default=now)
    updated_at: DatetimeField(required=True, rejected=True, default=now)
    moderator: BoolField(required=True, default=False, rejected=True)

    KEY_FIELD = "username"

    def touch(self):
        self.updated_at = now()

    def _before_save(self):
        self.touch()

    def create_auth_token(self):
        from .token import Token
        tokens = Token.find({"type": "auth", "user_id": self._id})
        for token in tokens:
            if not token.expired:
                return token
        token = Token(type="auth", user_id=self._id)
        token.save()
        return token

    def get_auth_token(self):
        from .token import Token
        tokens = Token.find({"type": "auth", "user_id": self._id})
        for token in tokens:
            if not token.expired:
                return token
        return None
