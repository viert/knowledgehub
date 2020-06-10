from uengine.utils import uuid4_string, now
from uengine.models.storable_model import StorableModel
from uengine.context import ctx

DEFAULT_TOKEN_EXPIRATION_TIME = 87600 * 7 * 2
DEFAULT_TOKEN_AUTO_PROLONGATION = True


class Token(StorableModel):

    FIELDS = (
        "token",
        "type",
        "user_id",
        "created_at",
        "updated_at",
    )

    KEY_FIELD = "token"

    REQUIRED_FIELDS = (
        "type",
        "token",
        "user_id",
        "created_at",
        "updated_at",
    )

    DEFAULTS = {
        "type": "auth",
        "token": uuid4_string,
        "created_at": now,
        "updated_at": now,
    }

    INDEXES = (
        ["token", {"unique": True}],
        ["user_id", "type"]
    )

    # pylint: disable=attribute-defined-outside-init
    def touch(self):
        self.updated_at = now()

    def _before_save(self):
        self.touch()
        self.invalidate()

    def _before_delete(self):
        self.invalidate()

    def prolongate(self):
        auto_prolongation = ctx.cfg.get("token_auto_prolongation", DEFAULT_TOKEN_AUTO_PROLONGATION)
        if auto_prolongation:
            self.save()

    @property
    def user(self):
        from .user import User
        return User.cache_get(self.user_id)

    @property
    def expired(self):
        expiration_time = ctx.cfg.get("token_expiration_time", DEFAULT_TOKEN_EXPIRATION_TIME)
        if expiration_time <= 0:
            return False

        auto_prolongation = ctx.cfg.get("token_auto_prolongation", DEFAULT_TOKEN_AUTO_PROLONGATION)
        token_lifetime_start = self.updated_at if auto_prolongation else self.created_at
        token_lifetime = now() - token_lifetime_start

        return token_lifetime.total_seconds() > expiration_time