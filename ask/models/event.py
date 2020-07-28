from typing import Union, Optional
from glasskit.utils import now
from glasskit.uorm.db import ObjectsCursor
from glasskit.uorm.models.submodel import StorableSubmodel
from glasskit.uorm.models.fields import ListField, StringField, ObjectIdField, BoolField, DictField, DatetimeField


class Event(StorableSubmodel):

    COLLECTION = "events"

    user_id: ObjectIdField(required=True, rejected=True, index=True)
    dismissed: BoolField(required=True, default=False)
    sent: DictField(required=True, rejected=True, default=dict)
    created_at: DatetimeField(required=True, rejected=True, default=now)

    INDEXES = (
        [[("user_id", 1), ("dismissed", False)], {}],
        [[("sent.email", 1)], {}],
        [[("sent.telegram", 1)], {}],
        [[("sent.icq", 1)], {}],
    )

    @property
    def user(self) -> Union['User', None]:
        return User.find_one({"_id": self.user_id})

    @classmethod
    def find_pending(cls, send_with: Union[None, str] = None) -> ObjectsCursor:
        key = "sent"
        if send_with:
            key = key + "." + send_with

        query = {key: False}
        return cls.find(query)


class TagNewQuestionEvent(Event):

    SUBMODEL = "tag_new_question_event"

    tags: ListField(required=True, rejected=True, min_length=1)
    question_id: ObjectIdField(required=True, rejected=True)

    @property
    def question(self) -> Optional['Question']:
        return Question.find_one({"_id": self.question_id})


class QuestionNewAnswerEvent(Event):

    SUBMODEL = "question_new_answer_event"

    question_id: ObjectIdField(required=True, rejected=True)
    answer_id: ObjectIdField(required=True, rejected=True)
    author_id: ObjectIdField(required=True, rejected=True)

    @property
    def question(self) -> 'Question':
        return Question.find_one({"_id": self.question_id})

    @property
    def answer(self) -> 'Answer':
        return Answer.find_one({"_id": self.answer_id})

    @property
    def author(self) -> 'User':
        return User.find_one({"_id": self.author_id})


class PostNewCommentEvent(Event):

    SUBMODEL = "post_new_comment_event"

    post_id: ObjectIdField(required=True, rejected=True)
    post_type: StringField(required=True, rejected=True)
    comment_id: ObjectIdField(required=True, rejected=True)
    author_id: ObjectIdField(required=True, rejected=True)

    @property
    def post(self) -> 'BasePost':
        return BasePost.find_one({"_id": self.post_id})

    @property
    def comment(self) -> 'Comment':
        return Comment.find_one({"_id": self.comment_id})

    @property
    def author(self) -> 'User':
        return User.find_one({"_id": self.author_id})


class MentionEvent(Event):

    SUBMODEL = "mention_event"

    post_id: ObjectIdField(required=True, rejected=True)
    post_type: StringField(required=True, rejected=True)
    author_id: ObjectIdField(required=True, rejected=True)

    @property
    def post(self) -> 'BasePost':
        return BasePost.find_one({"_id": self.post_id})

    @property
    def author(self) -> 'User':
        return User.find_one({"_id": self.author_id})


class AnswerAcceptedEvent(Event):

    SUBMODEL = "answer_accepted_event"

    answer_id: ObjectIdField(required=True, rejected=True)
    accepted_by_id: ObjectIdField(required=True, rejected=True)

    @property
    def answer(self) -> 'Answer':
        return Answer.find_one({"_id": self.answer_id})


Event.register_submodel(TagNewQuestionEvent.SUBMODEL, TagNewQuestionEvent)
Event.register_submodel(QuestionNewAnswerEvent.SUBMODEL, QuestionNewAnswerEvent)
Event.register_submodel(PostNewCommentEvent.SUBMODEL, PostNewCommentEvent)
Event.register_submodel(MentionEvent.SUBMODEL, MentionEvent)
Event.register_submodel(AnswerAcceptedEvent.SUBMODEL, AnswerAcceptedEvent)


from .user import User
from .post import Question, BasePost, Answer, Comment
