from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User, TagSubscription, UserSubscription


class TestUser(MongoMockTest):

    def setUp(self) -> None:
        TagSubscription.destroy_all()
        UserSubscription.destroy_all()
        User.destroy_all()

    def test_tag_subscription_is_created(self):
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

        u.destroy()
        self.assertEqual(TagSubscription.find().count(), 0)
        self.assertEqual(UserSubscription.find().count(), 0)
