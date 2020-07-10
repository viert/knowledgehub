import re
import requests
import random
from glasskit import ctx
from glasskit.commands import Command
from glasskit.queue import DummyQueue
from ask.tasks.worker import Worker
from ask.models import User, Comment, Question, Answer

USERS_COUNT = 20
QUESTION_COUNT = 20
MAX_ANSWERS = 5
MAX_COMMENTS = 10
MAX_TAGS = 3

wrk = Worker()


class Fixtures(Command):

    def init_argument_parser(self, parser):
        parser.add_argument("-d", "--drop", action="store_true", default=False)

    def drop(self):
        fx_users = User.find({"username": re.compile(r"^fx_test_user")})
        user_ids = [u._id for u in fx_users]
        ctx.log.info("dropping fixture comments")
        Comment.destroy_many({"author_id": {"$in": user_ids}})
        ctx.log.info("dropping fixture answers")
        Answer.destroy_many({"author_id": {"$in": user_ids}})
        ctx.log.info("dropping fixture questions")
        Question.destroy_many({"author_id": {"$in": user_ids}})
        ctx.log.info("dropping fixture users")
        User.destroy_many({"username": re.compile(r"^fx_test_user")})

    def random_user(self):
        idx = random.randrange(len(self.users))
        return self.users[idx]

    def create_users(self):
        ctx.log.info("creating fixture users")
        self.users = []
        data = requests.get(f"https://randomuser.me/api/?results={USERS_COUNT}").json()
        i = 1
        for user_data in data["results"]:
            username = f"fx_test_user_{i}"
            user = User.get(username)
            if not user:
                user = User(
                    username=username,
                    first_name=user_data["name"]["first"],
                    last_name=user_data["name"]["last"],
                    avatar_url=user_data["picture"]["thumbnail"],
                    email=user_data["email"]
                )
                user.save()
            self.users.append(user)
            i += 1

    @staticmethod
    def random_paragraph():
        text = requests.get("https://fish-text.ru/get?type=paragraph").json()["text"]
        return text.replace('\\n', '\n')

    def random_tags(self):
        count = random.randrange(MAX_TAGS)
        data = requests.get(f"https://random-word-api.herokuapp.com/word?number={count}").json()
        return data

    def create(self):
        self.create_users()
        ctx.log.info("generating questions")
        for iq in range(QUESTION_COUNT):
            title = requests.get("https://fish-text.ru/get?type=title").json()["text"]
            text = self.random_paragraph()
            tags = self.random_tags()
            q = Question(body=text, title=title, tags=tags, author_id=self.random_user()._id)
            q.save()
            for ic in range(random.randrange(MAX_COMMENTS)):
                text = requests.get("https://fish-text.ru/get?type=sentence").json()["text"]
                c = q.create_comment(author_id=self.random_user()._id, body=text)
                c.save()
            for ac in range(random.randrange(MAX_ANSWERS)):
                text = self.random_paragraph()
                a = q.create_answer(author_id=self.random_user()._id, body=text)
                a.save()
                for ic in range(random.randrange(MAX_COMMENTS)):
                    text = requests.get("https://fish-text.ru/get?type=sentence").json()["text"]
                    c = a.create_comment(author_id=self.random_user()._id, body=text)
                    c.save()
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    def run(self):
        del ctx.queue
        ctx.queue = DummyQueue({})
        if self.args.drop:
            self.drop()
        else:
            self.create()
