from uengine.tests.mongo_mock import MongoMockTest
from ask.models import User, Question, Tag, Answer, Comment
from ask.tasks.worker import run_task


class TestQuestion(MongoMockTest):

    @classmethod
    def setUpClass(cls):
        super(TestQuestion, cls).setUpClass()
        cls.user = User(username='test_user')
        cls.user.save()

    def run_tasks(self):
        from uengine import ctx
        for task in ctx.queue.tasks:
            run_task(task)

    def test_tags(self):
        q = Question(
            author_id=self.user._id,
            title='How to patch KDE on FreeBSD?',
            body="subj",
            tags=["kde", "freebsd", "anime"],
        )
        q.save()
        self.run_tasks()

        cnt = 0
        for tag in Tag.find():
            cnt += 1
            self.assertEqual(tag.questions_count, 1)
        self.assertEqual(cnt, len(q.tags))

        q2 = Question(
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
        self.assertEqual(Tag.find().count(), 0)
