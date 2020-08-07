from glasskit import ctx
from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User, Question, Tag, Answer, Comment
from ask.models.post import BasePost
from ask.tasks.worker import Worker

wrk = Worker()


class TestPost(MongoMockTest):

    @classmethod
    def setUpClass(cls):
        super(TestPost, cls).setUpClass()
        cls.user = User({"username": "test_user", "ext_id": "test_user"})
        cls.user.save()

    def setUp(self) -> None:
        BasePost.destroy_all()
        Tag.destroy_all()

    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    def test_substitutions(self):
        ctx.cfg["substitutions"] = (
            (r"\b([A-Z]+-\d+)\b", r"[\1](https://jira.example.com/browse/\1)"),
        )

        q = Question.create(
            author_id=self.user._id,
            title='How to patch KDE on FreeBSD?',
            body="Is that exactly what is meant in MYPROJ-338?",
            tags=["kde", "freebsd", "anime"],
        )

        q.save()
        self.run_tasks()

        self.assertEqual(q.body,
                         "Is that exactly what is meant in "
                         "[MYPROJ-338](https://jira.example.com/browse/MYPROJ-338)?")

        a = q.create_answer({
            "author_id": self.user._id,
            "body": "No, it's not. It's actually MYPROJ-42"
        })
        a.save()
        self.run_tasks()

        self.assertEqual(a.body,
                         "No, it's not. It's actually "
                         "[MYPROJ-42](https://jira.example.com/browse/MYPROJ-42)")
        a.save()

        c = a.create_comment({
            "author_id": self.user._id,
            "body": "MYPROJ-338 looks more promising. Well, MYPROJ-42 is OK too.",
        })

        c.save()
        self.run_tasks()

        self.assertEqual(c.body,
                         "MYPROJ-338 looks more promising. Well, MYPROJ-42 is OK too.")
