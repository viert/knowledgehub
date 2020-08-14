from glasskit.tests.mongo_mock_test import MongoMockTest
from glasskit import ctx
from ask import app, force_init_app
from ask.tasks.worker import Worker
from ask.models import User

wrk = Worker()


class HTTPAPITestCase(MongoMockTest):

    @classmethod
    def setUpClass(cls) -> None:
        force_init_app()
        super().setUpClass()
        User.ensure_indexes()
        cls.app = app

    def setUp(self) -> None:
        User.destroy_all()
        self.user1 = User({"username": "user1", "ext_id": "user1"})
        self.user1.save()
        self.user1.create_auth_token()
        self.user2 = User({"username": "user2", "ext_id": "user2"})
        self.user2.save()
        self.user2.create_auth_token()
        self.moderator = User({"username": "mod", "ext_id": "mod", "moderator": True})
        self.moderator.save()
        self.moderator.create_auth_token()


    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    @staticmethod
    def clear_task_queue():
        for task in ctx.queue.tasks:
            try:
                wrk.run_task(task)
            except:
                pass

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
