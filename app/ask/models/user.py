from typing import Optional, List
from glasskit.utils import now
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import StringField, BoolField, DatetimeField
from ask.errors import AlreadySubscribed, NotSubscribed, IntegrityError


class User(StorableModel):

    ext_id: StringField(required=True, rejected=True, unique=True)
    username: StringField(required=True, unique=True)
    first_name: StringField(default="")
    last_name: StringField(default="")
    avatar_url: StringField(default="")
    created_at: DatetimeField(required=True, rejected=True, default=now)
    updated_at: DatetimeField(required=True, rejected=True, default=now)
    moderator: BoolField(required=True, default=False, rejected=True)
    email: StringField(default="", restricted=True)
    telegram_id: StringField(default=None, restricted=True)
    icq_id: StringField(default=None, restricted=True)

    KEY_FIELD = "username"

    def touch(self):
        self.updated_at = now()

    def fixup_username(self):
        idx = 0
        while True:
            username = self.username
            if idx > 0:
                username = username + f"_{idx}"
            ex = User.find_one({"username": username})
            if not ex or ex._id == self._id:
                self.username = username
                break
            idx += 1

    def _before_save(self):
        ex = User.find_one({"username": self.username})
        if ex and ex._id != self._id:
            raise IntegrityError("username has already been taken")
        self.touch()

    def _after_save(self, is_new):
        if is_new:
            self.create_subscriptions()

    def create_subscriptions(self):
        if not self.tag_subscription:
            TagSubscription({"user_id": self._id}).save()
        if not self.user_subscription:
            UserSubscription({"user_id": self._id}).save()

    def _before_delete(self):
        self.tag_subscription.destroy()
        self.user_subscription.destroy()

    def create_auth_token(self):
        from .token import Token
        tokens = Token.find({"type": "auth", "user_id": self._id})
        for token in tokens:
            if not token.expired:
                return token
        token = Token({"type": "auth", "user_id": self._id})
        token.save()
        return token

    def get_auth_token(self):
        from .token import Token
        tokens = Token.find({"type": "auth", "user_id": self._id})
        for token in tokens:
            if not token.expired:
                return token
        return None

    @property
    def tag_subscription(self) -> 'TagSubscription':
        return TagSubscription.find_one({"user_id": self._id})

    @property
    def user_subscription(self) -> 'UserSubscription':
        return UserSubscription.find_one({"user_id": self._id})

    def subscribe_to_user(self, other: 'User') -> None:
        us = self.user_subscription
        if other._id in us.subs_user_ids:
            raise AlreadySubscribed("you are already subscribed to this user")
        us.subs_user_ids.append(other._id)
        us.save()

    def unsubscribe_from_user(self, other: 'User') -> None:
        us = self.user_subscription
        if other._id not in us.subs_user_ids:
            raise NotSubscribed("you are not subscribed to this user")
        us.subs_user_ids.remove(other._id)
        us.save()

    def subscribe_to_tag(self, tag: str) -> None:
        ts = self.tag_subscription
        if tag in ts.tags:
            raise AlreadySubscribed("you are already subscribed to this tag")
        ts.tags.append(tag)
        ts.save()

    def unsubscribe_from_tag(self, tag: str) -> None:
        ts = self.tag_subscription
        if tag not in ts.tags:
            raise NotSubscribed("you are not subscribed to this tag")
        ts.tags.remove(tag)
        ts.save()

    def replace_tags(self, tags: List[str]) -> None:
        ts = self.tag_subscription
        ts.tags = tags
        ts.save()

    def get_new_events(self):
        return Event.find({"user_id": self._id, "dismissed": False})

    @classmethod
    def find_by_telegram_id(cls, telegram_id: str) -> Optional['User']:
        return cls.find_one({
            "$or": [
                {"telegram_id": telegram_id},
                {"telegram_id": "@" + telegram_id},
            ]
        })

    @classmethod
    def find_by_icq_id(cls, icq_id: str) -> Optional['User']:
        return cls.find_one({"icq_id": icq_id})

    def chat(self, network_type: str) -> Optional['Chat']:
        return Chat.find_one({"user_id": self._id, "network_type": network_type})

    def telegram(self):
        return self.chat("telegram")

    def icq(self):
        return self.chat("icq")


from .tag_subscription import TagSubscription
from .user_subscription import UserSubscription
from .event import Event
from .chat import Chat