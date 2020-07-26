import re
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import StringField, IntField
from glasskit.uorm.utils import save_required
from glasskit import ctx
from ask.errors import HasReferences, InvalidTags


TAG_NAME_EXPRESSION = r"[^\W_](?:(?:[^\W_]|-)*[^\W_])?"
TAG_NAME_RE = re.compile("^" + TAG_NAME_EXPRESSION + "$")


class Tag(StorableModel):

    name: StringField(required=True, rejected=True, min_length=1, unique=True)
    questions_count: IntField(required=True, rejected=True, default=0)
    subscribers_count: IntField(required=True, rejected=True, default=0)
    description: StringField()

    KEY_FIELD = "name"

    def questions(self, include_deleted=False):
        query = {"tags": self.name}
        if not include_deleted:
            query["deleted"] = False
        return Question.find({"tags": self.name})

    @save_required
    def recalculate_questions_count(self):
        q_count = self.questions().count()
        if q_count != self.questions_count:
            self.questions_count = q_count
            self.save(skip_callback=True)

    def subscriptions(self):
        return TagSubscription.find({"tags": self.name})

    @save_required
    def recalculate_subscribers(self):
        s_count = self.subscriptions().count()
        if s_count != self.subscribers_count:
            self.subscribers_count = s_count
            self.save(skip_callback=True)

    def _before_save(self):
        if not TAG_NAME_RE.match(self.name):
            raise InvalidTags(f"tag name {self.name} is invalid")
        if self.description is None:
            self.description = f"Questions related to {self.name}"
        self.questions_count = self.questions().count()
        self.subscribers_count = self.subscriptions().count()

    def _before_delete(self):
        if self.questions().count() > 0:
            raise HasReferences("tag has references")
        if self.subscriptions().count() > 0:
            raise HasReferences("tag has references")

    def empty(self) -> bool:
        return self.questions_count == 0 and self.subscribers_count == 0

    @classmethod
    def sync(cls, tags):
        """
        This is designed to be called from background tasks
        """
        for tag in tags:
            t: 'Tag' = cls.get(tag)
            if t is None:
                cls({"name": tag}).save()
                ctx.log.info("tag %s has been created", tag)
            else:
                t.recalculate_subscribers()
                t.recalculate_questions_count()

    @classmethod
    def full_sync(cls):
        """
        This is designed to be called from shell only
        """
        tags_set = set()
        for tag in cls.find():
            tags_set.add(tag.name)
        for ts in TagSubscription.find():
            for tag in ts.tags:
                tags_set.add(tag)
        for q in Question.find():
            for tag in q.tags:
                tags_set.add(tag)
        cls.sync(tags_set)

        for tag in cls.find():
            if tag.empty():
                ctx.log.info("tag %s destroyed due to having no references", tag.name)
                tag.destroy()


from .tag_subscription import TagSubscription
from .post import Question
