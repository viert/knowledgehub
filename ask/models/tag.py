from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.fields import StringField, IntField
from glasskit.uorm.errors import DoNotSave
from glasskit.uorm.utils import save_required
from ask.errors import HasReferences


class Tag(StorableModel):

    name: StringField(required=True, rejected=True, min_length=1, unique=True)
    questions_count: IntField(required=True, rejected=True, default=0)
    subscribers_count: IntField(required=True, rejected=True, default=0)

    KEY_FIELD = "name"

    def questions(self):
        from .post import Question
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
        self.questions_count = self.questions().count()
        self.subscribers_count = self.subscriptions().count()

    def _before_delete(self):
        if self.questions().count() > 0:
            raise HasReferences("tag has references")
        if self.subscriptions().count() > 0:
            raise HasReferences("tag has references")

    @classmethod
    def sync(cls, tags):
        """
        This is designed to be called from background tasks
        """
        for tag in tags:
            t: 'Tag' = cls.get(tag)
            if t is None:
                cls({"name": tag}).save()
            else:
                t.recalculate_subscribers()
                t.recalculate_questions_count()


from .tag_subscription import TagSubscription
