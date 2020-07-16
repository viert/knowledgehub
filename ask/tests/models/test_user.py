from glasskit import ctx
from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User, TagSubscription, UserSubscription, Tag
from ask.tasks.worker import Worker

wrk = Worker()


class TestUser(MongoMockTest):

    def setUp(self) -> None:
        TagSubscription.destroy_all()
        UserSubscription.destroy_all()
        User.destroy_all()

    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    def test_subscription_objects_are_created(self):
        self.assertEqual(TagSubscription.find().count(), 0)
        self.assertEqual(UserSubscription.find().count(), 0)
        u = User({"username": "test", "ext_id": "test"})
        u.save()

        ts = u.tag_subscription
        self.assertIsNotNone(ts)
        self.assertCountEqual(ts.tags, [])

        us = u.user_subscription
        self.assertIsNotNone(us)
        self.assertCountEqual(us.subs_user_ids, [])

        self.assertEqual(TagSubscription.find().count(), 1)
        self.assertEqual(UserSubscription.find().count(), 1)

        u.subscribe_to_tag("hello")
        self.run_tasks()
        t: Tag = Tag.get("hello")
        self.assertIsNotNone(t)
        self.assertEqual(t.subscribers_count, 1)

        u.destroy()
        self.run_tasks()

        self.assertEqual(TagSubscription.find().count(), 0)
        self.assertEqual(UserSubscription.find().count(), 0)

        t = Tag.get("hello")
        self.assertEqual(t.subscribers_count, 0)
