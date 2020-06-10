from uengine.models.storable_model import StorableModel
from uengine.models.abstract_model import DoNotSave, save_required
from ask.errors import HasReferences


class Tag(StorableModel):

    FIELDS = (
        "_id",
        "name",
        "questions_count",
    )

    DEFAULTS = {
        "questions_count": 0
    }

    REQUIRED_FIELDS = (
        "name",
    )

    KEY_FIELD = "name"

    INDEXES = (
        ["name", {"unique": True}],
    )

    def questions(self):
        from .post import Question
        return Question.find({"tags": self.name})

    @save_required
    def recalculate_questions_count(self):
        qcount = self.questions().count()
        if qcount != self.questions_count:
            self.questions_count = qcount
            if self.questions_count == 0:
                self.destroy(skip_callback=True)
            else:
                self.save(skip_callback=True)

    def _before_save(self):
        self.questions_count = self.questions().count()
        if self.questions_count == 0:
            if not self.is_new:
                self.destroy()
            raise DoNotSave()

    def _before_delete(self):
        if self.questions().count() > 0:
            raise HasReferences("tag has references")

    @classmethod
    def sync(cls, tags):
        """
        This is designed to be called from background tasks
        """
        for tag in tags:
            t = cls.get(tag)
            if t is None:
                cls(name=tag).save()
            else:
                t.recalculate_questions_count()
