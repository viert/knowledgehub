from glasskit import ctx
from glasskit.tests.mongo_mock_test import MongoMockTest
from ask.models import User, Question
from ask.models.post import BasePost
from ask.models.event import TagNewQuestionEvent, Event, QuestionNewAnswerEvent, PostNewCommentEvent
from ask.tasks.worker import Worker

wrk = Worker()


class TestEvent(MongoMockTest):

    def setUp(self) -> None:
        super(TestEvent, self).setUp()
        Event.destroy_all()
        BasePost.destroy_all()
        User.destroy_all()
        self.clear_queue()

    def clear_queue(self):
        for task in ctx.queue.tasks:
            try:
                wrk.run_task(task)
            except:
                pass

    @staticmethod
    def run_tasks():
        for task in ctx.queue.tasks:
            wrk.run_task(task)

    def test_tag_new_post_event(self):
        u = User({"username": "test", "ext_id": "test"})
        u.save()
        u.subscribe_to_tag("test-tag")
        u.subscribe_to_tag("test-tag2")
        u.subscribe_to_tag("test-tag3")

        p = Question({
            "title": "test title",
            "body": "test body, needs to be long",
            "tags": ["test-tag", "test-tag2"],
            "author_id": u._id
        })
        p.save()
        self.run_tasks()

        events = u.get_new_events()
        self.assertEqual(events.count(), 0)

        other_user = User({"username": "other", "ext_id": "other"})
        other_user.save()

        p = Question({
            "title": "test title",
            "body": "test body, needs to be long",
            "tags": ["test-tag", "test-tag2"],
            "author_id": other_user._id
        })
        p.save()
        self.run_tasks()
        events = u.get_new_events()
        self.assertEqual(events.count(), 1)
        event: TagNewQuestionEvent = events[0]

        # only subscribed tags are listed in event
        self.assertCountEqual(event.tags, ["test-tag", "test-tag2"])
        self.assertEqual(event.question_id, p._id)

    def test_question_new_answer_event(self):
        user = User({"username": "test", "ext_id": "test"})
        user.save()
        other_user = User({"username": "other", "ext_id": "other"})
        other_user.save()

        p = Question({
            "title": "test title",
            "body": "test body, needs to be long",
            "tags": ["test-tag", "test-tag2"],
            "author_id": user._id
        })
        p.save()
        self.run_tasks()
        Event.destroy_all()

        a = p.create_answer({
            "body": "this is a self-answer, should not generate events",
            "author_id": user._id
        })
        a.save()
        self.run_tasks()

        events = user.get_new_events()
        self.assertEqual(events.count(), 0)

        a = p.create_answer({
            "body": "this is an answer by somebody else",
            "author_id": other_user._id
        })
        a.save()
        self.run_tasks()

        events = user.get_new_events()
        self.assertEqual(events.count(), 1)

        event: QuestionNewAnswerEvent = events[0]
        self.assertEqual(event.question_id, p._id)
        self.assertEqual(event.answer_id, a._id)
        self.assertEqual(event.author_id, other_user._id)

    def test_post_comment_event(self):
        user = User({"username": "test", "ext_id": "test"})
        user.save()
        other_user = User({"username": "other", "ext_id": "other"})
        other_user.save()

        p = Question({
            "title": "test title",
            "body": "test body, needs to be long",
            "tags": ["test-tag", "test-tag2"],
            "author_id": user._id
        })
        p.save()
        self.run_tasks()
        Event.destroy_all()

        c = p.create_comment({
            "body": "this is a self-comment, should not generate events",
            "author_id": user._id
        })
        c.save()
        self.run_tasks()

        events = user.get_new_events()
        self.assertEqual(events.count(), 0)

        c = p.create_comment({
            "body": "this is a real comment, should generate an event",
            "author_id": other_user._id
        })
        c.save()
        self.run_tasks()

        events = user.get_new_events()
        self.assertEqual(events.count(), 1)

        event: PostNewCommentEvent = events[0]
        self.assertEqual(event.post_id, p._id)
        self.assertEqual(event.comment_id, c._id)
        self.assertEqual(event.author_id, other_user._id)
