from glasskit.tests.mongo_mock_test import MongoMockTest
from glasskit import ctx
from ask import app, force_init_app
from ask.tasks.worker import Worker
from ask.models import User

wrk = Worker()


class HTTPAPITestCase(MongoMockTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        User.ensure_indexes()
        force_init_app()
        cls.app = app

        cls.user1 = User({"username": "user1", "ext_id": "user1"})
        cls.user1.save()
        cls.user1.create_auth_token()
        cls.user2 = User({"username": "user2", "ext_id": "user2"})
        cls.user2.save()
        cls.user2.create_auth_token()
        cls.moderator = User({"username": "mod", "ext_id": "mod", "moderator": True})
        cls.moderator.save()
        cls.moderator.create_auth_token()

    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    @property
    def client(self):
        return self.app.flask.test_client()

    def request(self, method, path, headers=None, user=None, json=None):
        if headers is None:
            headers = {}
        if user is not None:
            headers["X-Api-Auth-Token"] = user.get_auth_token().token
        kwargs = {"headers": headers, "method": method}

        if json is not None:
            kwargs["json"] = json
            headers["Content-Type"] = "application/json"

        return self.client.open(path, **kwargs)

    def get(self, path, user=None):
        return self.request("GET", path, user=user)

    def post(self, path, user=None, json=None):
        return self.request("POST", path, user=user, json=json)

    def patch(self, path, user=None, json=None):
        return self.request("PATCH", path, user=user, json=json)

    def put(self, path, user=None, json=None):
        return self.request("PUT", path, user=user, json=json)

    def delete(self, path, user=None, json=None):
        return self.request("DELETE", path, user=user, json=json)
