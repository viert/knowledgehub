from uengine.utils import now
from uengine.models.storable_model import StorableModel


class User(StorableModel):

    FIELDS = (
        "_id",
        "ext_id",
        "username",
        "first_name",
        "last_name",
        "email",
        "avatar_url",
        "created_at",
        "updated_at",
        "supervisor",
        "moderator",
    )

    KEY_FIELD = "username"

    DEFAULTS = {
        "first_name": "",
        "last_name": "",
        "avatar_url": "",
        "supervisor": False,
        "moderator": False,
        "email": "",
        "ext_id": None,
        "created_at": now,
        "updated_at": now,
    }

    REJECTED_FIELDS = (
        "password_hash",
        "supervisor",
        "created_at",
        "updated_at",
    )

    REQUIRED_FIELDS = (
        "username",
    )

    VALIDATION_TYPES = {
        "supervisor": bool,
        "moderator": bool,
    }

    INDEXES = (
        ["username", {"unique": True}],
        "ext_id",
    )

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
