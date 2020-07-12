from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User, TagSubscription


class TestUser(MongoMockTest):

    def setUp(self) -> None:
        TagSubscription.destroy_all()
        User.destroy_all()

    def test_tag_subscription_is_created(self):
        u = User({"username": "test", "ext_id": "test"})
        u.save()

        ts = u.tag_subscription
        self.assertIsNotNone(ts)
        self.assertCountEqual(ts.tags, [])

