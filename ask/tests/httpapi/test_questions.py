from .httpapi_testcase import HTTPAPITestCase
from ask.models import Question, Answer, Tag


class TestQuestions(HTTPAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        Question.destroy_all()

    def create_questions(self):
        q1 = Question({"title": "question1", "body": "is this the real life?",
                       "author_id": self.user1._id, "tags": ["queen"]})
        q1.save()
        q2 = Question({"title": "question2", "body": "is this just fantasy?",
                       "author_id": self.user1._id, "tags": ["queen"]})
        q2.save()

        q3 = Question({"title": "question3", "body": "Scaramouch, scaramouch will you do the fandango?",
                       "author_id": self.user2._id, "tags": ["queen"]})
        q3.save()

        return q1, q2, q3

    def test_questions_list(self):
        self.create_questions()

        resp = self.get("/api/v1/questions/")
        self.assertEqual(resp.status_code, 200, resp.data)
        data = resp.json
        self.assertIn("authors", data)
        self.assertIn("questions", data)

        authors = data["authors"]
        self.assertEqual(len(authors["data"]), 2)

        questions = data["questions"]
        self.assertEqual(questions["count"], 3)

    def test_questions_list_mine(self):
        self.create_questions()
        resp = self.get("/api/v1/questions/?_mine=true", user=self.user2)
        self.assertEqual(resp.status_code, 200, resp.data)
        data = resp.json
        self.assertIn("authors", data)
        self.assertIn("questions", data)

        authors = data["authors"]
        self.assertEqual(len(authors["data"]), 1)

        questions = data["questions"]
        self.assertEqual(questions["count"], 1)

    def test_update_post(self):
        q1, _, _ = self.create_questions()
        payload = {
            "body": "this question was modified due to our rules"
        }

        resp = self.patch(f"/api/v1/questions/{q1._id}", json=payload)
        self.assertEqual(resp.status_code, 401)

        resp = self.patch(f"/api/v1/questions/{q1._id}", json=payload, user=self.user2)
        self.assertEqual(resp.status_code, 403)

        resp = self.patch(f"/api/v1/questions/{q1._id}", json=payload, user=self.moderator)
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertEqual(q1.body, payload["body"])
        self.assertEqual(q1.edited_by_id, self.moderator._id)

        payload = {
            "body": "i still wonder if this is the real life"
        }

        resp = self.patch(f"/api/v1/questions/{q1._id}", json=payload, user=self.user1)
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertEqual(q1.body, payload["body"])
        self.assertEqual(q1.edited_by_id, self.user1._id)

    def test_delete_and_restore_question(self):
        q1, _, _ = self.create_questions()
        resp = self.delete(f"/api/v1/questions/{q1._id}")
        self.assertEqual(resp.status_code, 401)

        resp = self.delete(f"/api/v1/questions/{q1._id}", user=self.user1)
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertTrue(q1.deleted)
        self.assertEqual(q1.deleted_by_id, self.user1._id)

        q1.restore()
        resp = self.delete(f"/api/v1/questions/{q1._id}", user=self.moderator)
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertTrue(q1.deleted)
        self.assertEqual(q1.deleted_by_id, self.moderator._id)

        resp = self.post(f"/api/v1/questions/{q1._id}/restore")
        self.assertEqual(resp.status_code, 401)

        resp = self.post(f"/api/v1/questions/{q1._id}/restore", user=self.user1)
        self.assertEqual(resp.status_code, 403)

        resp = self.post(f"/api/v1/questions/{q1._id}/restore", user=self.moderator)
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertFalse(q1.deleted)
        self.assertIsNone(q1.deleted_by_id)
        self.assertIsNone(q1.deleted_at)

    def test_vote_question(self):
        q1, _, _ = self.create_questions()

        resp = self.post(f"/api/v1/questions/{q1._id}/vote", json={"value": 1})
        self.assertEqual(resp.status_code, 401)

        resp = self.post(f"/api/v1/questions/{q1._id}/vote", user=self.user1, json={"value": 1})
        self.assertEqual(resp.status_code, 403)

        resp = self.post(f"/api/v1/questions/{q1._id}/vote", user=self.user2, json={"value": 1})
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertEqual(q1.points, 1)

        resp = self.post(f"/api/v1/questions/{q1._id}/vote", user=self.moderator, json={"value": 1})
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertEqual(q1.points, 2)

        resp = self.post(f"/api/v1/questions/{q1._id}/vote", user=self.user2, json={"value": -1})
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertEqual(q1.points, 0)

    def test_create_question(self):
        attrs = {
            "title": "a real question",
            "body": "what is the meaning of life and everything",
            "tags": ["guide"]
        }
        resp = self.post(f"/api/v1/questions/", json=attrs)
        self.assertEqual(resp.status_code, 401)

        resp = self.post(f"/api/v1/questions/", json=attrs, user=self.user1)
        self.assertEqual(resp.status_code, 200)
        self.run_tasks()

        data = resp.json
        q = Question.get(data["data"]["_id"])
        self.assertEqual(q.body, attrs["body"])
        self.assertEqual(q.title, attrs["title"])
        self.assertCountEqual(q.tags, attrs["tags"])

        t: Tag = Tag.get("guide")
        self.assertIsNotNone(t)
        self.assertEqual(t.questions_count, 1)

    def test_create_answer(self):
        q1, _, _ = self.create_questions()

        attrs = {
            "body": "I have something to show you"
        }

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/", json=attrs)
        self.assertEqual(resp.status_code, 401)

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/", user=self.user1, json=attrs)
        self.assertEqual(resp.status_code, 200)

        q1.reload()
        self.assertEqual(q1.answers_count, 1)

        a: Answer = q1.answers[0]
        self.assertEqual(a.body, attrs["body"])

    def test_update_answer(self):
        q1, _, _ = self.create_questions()
        a = q1.create_answer({"body": "I have something to show you", "author_id": self.user2._id})
        a.save()

        attrs = {"body": "this post has been modified due to our rules"}

        resp = self.patch(f"/api/v1/questions/{q1._id}/answers/{a._id}", json=attrs)
        self.assertEqual(resp.status_code, 401)

        resp = self.patch(f"/api/v1/questions/{q1._id}/answers/{a._id}", user=self.user1, json=attrs)
        self.assertEqual(resp.status_code, 403)

        resp = self.patch(f"/api/v1/questions/{q1._id}/answers/{a._id}", user=self.moderator, json=attrs)
        self.assertEqual(resp.status_code, 200)

        a.reload()
        self.assertEqual(a.body, attrs["body"])
        self.assertEqual(a.edited_by_id, self.moderator._id)

    def test_delete_answer(self):
        q1, _, _ = self.create_questions()
        a = q1.create_answer({"body": "I have something to show you", "author_id": self.user2._id})
        a.save()

        resp = self.delete(f"/api/v1/questions/{q1._id}/answers/{a._id}")
        self.assertEqual(resp.status_code, 401)

        resp = self.delete(f"/api/v1/questions/{q1._id}/answers/{a._id}", user=self.user1)
        self.assertEqual(resp.status_code, 403)

        resp = self.delete(f"/api/v1/questions/{q1._id}/answers/{a._id}", user=self.moderator)
        self.assertEqual(resp.status_code, 200)

        a.reload()
        self.assertTrue(a.deleted)
        self.assertEqual(a.deleted_by_id, self.moderator._id)

    def test_accept_answer(self):
        q1, _, _ = self.create_questions()
        a1 = q1.create_answer({"body": "I have something to show you", "author_id": self.user2._id})
        a1.save()
        a2 = q1.create_answer({"body": "Correct answer", "author_id": self.moderator._id})
        a2.save()

        self.assertFalse(q1.has_accepted_answer)
        self.assertFalse(a1.accepted)

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/{a1._id}/accept")
        self.assertEqual(resp.status_code, 401)

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/{a1._id}/accept", user=self.user2)
        self.assertEqual(resp.status_code, 403)

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/{a1._id}/accept", user=self.user1)
        self.assertEqual(resp.status_code, 200)

        a1.reload()
        a2.reload()
        q1.reload()

        self.assertTrue(q1.has_accepted_answer)
        self.assertTrue(a1.accepted)
        self.assertFalse(a2.accepted)

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/{a2._id}/accept", user=self.user1)
        self.assertEqual(resp.status_code, 200)

        a1.reload()
        a2.reload()
        q1.reload()

        self.assertTrue(q1.has_accepted_answer)
        self.assertFalse(a1.accepted)
        self.assertTrue(a2.accepted)

        resp = self.post(f"/api/v1/questions/{q1._id}/answers/{a2._id}/revoke", user=self.user1)
        self.assertEqual(resp.status_code, 200)

        a1.reload()
        a2.reload()
        q1.reload()

        self.assertFalse(q1.has_accepted_answer)
        self.assertFalse(a1.accepted)
        self.assertFalse(a2.accepted)
