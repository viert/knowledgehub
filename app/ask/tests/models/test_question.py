from glasskit import ctx
from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User, Question, Tag
from ask.models.post import BasePost
from ask.tasks.worker import Worker

wrk = Worker()


class TestQuestion(MongoMockTest):

    @classmethod
    def setUpClass(cls):
        super(TestQuestion, cls).setUpClass()
        cls.user = User({"username": "test_user", "ext_id": "test_user"})
        cls.user.save()

    def setUp(self) -> None:
        BasePost.destroy_all()
        Tag.destroy_all()

    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    def test_tags(self):
        q = Question.create(
            author_id=self.user._id,
            title='How to patch KDE on FreeBSD?',
            body="subjxxxxxx",
            tags=["kde", "freebsd", "anime"],
        )
        q.save()
        self.run_tasks()

        cnt = 0
        for tag in Tag.find():
            cnt += 1
            self.assertEqual(tag.questions_count, 1)
        self.assertEqual(cnt, len(q.tags))

        q2 = Question.create(
            author_id=self.user._id,
            title='TCPDump on FreeBSD',
            body="Does FreeBSD has a linux-like tcpdump or it's been as usual",
            tags=["freebsd", "tcpdump"],
        )
        q2.save()
        self.run_tasks()

        t = Tag.get("freebsd")
        self.assertEqual(t.questions_count, 2)

        q2.destroy()
        q.destroy()
        self.run_tasks()
        self.assertEqual(Tag.find().count(), 4)  # tags are not deleted automatically anymore

    def test_hrid(self):
        q = Question.create(
            author_id=self.user._id,
            title='How to patch KDE on FreeBSD?',
            body="subjxxxxxx",
            tags=["kde", "freebsd", "anime"],
        )
        q.save()
        self.run_tasks()
        self.assertEqual(q.human_readable_id, "how-to-patch-kde-on-freebsd")

        q = Question.create(
            author_id=self.user._id,
            title='How to patch KDE on FreeBSD?',
            body="subjxxxxxx",
            tags=["kde", "freebsd", "anime"],
        )
        q.save()
        self.run_tasks()
        self.assertEqual(q.human_readable_id, "how-to-patch-kde-on-freebsd_1")
