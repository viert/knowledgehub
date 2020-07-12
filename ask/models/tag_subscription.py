from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import ObjectIdField, ListField
from glasskit.errors import InputDataError
from ask.errors import InvalidTags
from ask.tasks import SyncTagsTask


class TagSubscription(StorableModel):

    USE_INITIAL_STATE = True

    tags: ListField(required=True, default=list, index=True)
    user_id: ObjectIdField(required=True, unique=True)  # unique means one-to-one relation

    def setup_initial_state(self):
        return {"tags": self.tags[:]}

    @property
    def user(self) -> 'User':
        return User.find_one({"_id": self.user_id})

    def _before_save(self):
        if self.user is None:
            raise InputDataError("user_id is invalid or user not found")
        if len(self.tags) != len(set(self.tags)):
            raise InvalidTags("tag list must be unique")
        new_tags = set(self.tags)
        old_tags = set(self._initial_state["tags"])
        if new_tags != old_tags:
            self._tags_changed = new_tags.union(old_tags)
        else:
            self._tags_changed = set()

    def _after_save(self, is_new):
        # create task only after assuring the new data is saved to db
        if self._tags_changed:
            task = SyncTagsTask.create(self._tags_changed)
            task.publish()


from .user import User
