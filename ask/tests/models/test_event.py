from glasskit import ctx
from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User
from ask.models.event import TagNewQuestionEvent
from ask.tasks.worker import Worker

wrk = Worker()


class TestEvent(MongoMockTest):
    @classmethod
    def setUpClass(cls):
        super(TestEvent, cls).setUpClass()

    def setUp(self) -> None:
        super(TestEvent, self).setUp()

    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    def test_tag_new_post_event(self):
        u = User({"username": "test", "ext_id": "test"})
        u.save()
        u.subscribe_to_tag("test-tag")

