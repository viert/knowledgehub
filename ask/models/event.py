from typing import Union, Optional, Dict
from glasskit import ctx
from glasskit.utils import now
from glasskit.uorm.models.submodel import StorableSubmodel
from glasskit.uorm.models.fields import ListField, StringField, ObjectIdField, BoolField, DictField, DatetimeField


class Event(StorableSubmodel):

    COLLECTION = "events"
    API_FIELDS = None

    user_id: ObjectIdField(required=True, rejected=True, index=True)
    dismissed: BoolField(required=True, default=False)
    sent: DictField(required=True, rejected=True, default=lambda: {"telegram": False, "icq": False})
    created_at: DatetimeField(required=True, rejected=True, default=now)

    INDEXES = (
        [[("user_id", 1), ("dismissed", False)], {}],
        [[("sent.email", 1)], {}],
        [[("sent.telegram", 1)], {}],
        [[("sent.icq", 1)], {}],
    )

    @property
    def type(self) -> str:
        return self.submodel

    @property
    def user(self) -> Union['User', None]:
        return User.find_one({"_id": self.user_id})

    def _after_save(self, is_new) -> None:
        if is_new:
            ctx.log.debug("%s created: %s", self.__class__.__name__, self.to_dict())

    def api_dict(self) -> Dict[str, str]:
        api_fields = list(self.API_FIELDS) + ["_id", "type", "created_at", "dismissed"]
        return self.to_dict(fields=api_fields)

    def dismiss(self):
        self.dismissed = True
        self.save(skip_callback=True)

    @classmethod
    def find_ready_to_send(cls, network_type: str):
        query = {
            "dismissed": False,
            f"sent.{network_type}": False
        }
        return cls.find(query).sort("created_at", 1)

    @staticmethod
    def base_uri():
        return ctx.cfg.get("base_uri", "http://localhost:8080")

    def telegram_text(self) -> str:
        pass

    def icq_text(self) -> str:
        pass


class TagNewQuestionEvent(Event):

    SUBMODEL = "tag_new_question_event"

    API_FIELDS = (
        'tags',
        'question_human_readable_id',
        'question_title',
        'author_username'
    )

    tags: ListField(required=True, rejected=True, min_length=1)
    question_id: ObjectIdField(required=True, rejected=True)

    @property
    def question(self) -> Optional['Question']:
        return Question.find_one({"_id": self.question_id})

    @property
    def question_title(self) -> str:
        return self.question.title

    @property
    def author_username(self) -> str:
        return self.question.author.username

    @property
    def question_human_readable_id(self):
        return self.question.human_readable_id

    def telegram_text(self) -> str:
        question_link = f"{self.base_uri()}/#/questions/{self.question_human_readable_id}?dismiss={self._id}"
        tags = ", ".join([f"*{tag}*" for tag in self.tags])
        return f"A new question [{self.question_title}]({question_link}) tagged with {tags} " \
               f"was published by *{self.author_username}*"

    def icq_text(self) -> str:
        question_link = f"{self.base_uri()}/#/questions/{self.question_human_readable_id}?dismiss={self._id}"
        tags = ", ".join([f"'{tag}'" for tag in self.tags])
        return f"A new question '{self.question_title}' tagged with {tags} was published " \
               f"by {self.author_username}:\n{question_link}"


class QuestionNewAnswerEvent(Event):

    SUBMODEL = "question_new_answer_event"

    API_FIELDS = (
        'question_id',
        'question_human_readable_id',
        'question_title',
        'answer_id',
        'author_username',
    )

    question_id: ObjectIdField(required=True, rejected=True)
    answer_id: ObjectIdField(required=True, rejected=True)
    author_id: ObjectIdField(required=True, rejected=True)

    @property
    def question(self) -> 'Question':
        return Question.find_one({"_id": self.question_id})

    @property
    def question_title(self) -> str:
        return self.question.title

    @property
    def question_human_readable_id(self) -> str:
        return self.question.human_readable_id

    @property
    def answer(self) -> 'Answer':
        return Answer.find_one({"_id": self.answer_id})

    @property
    def author(self) -> 'User':
        return User.find_one({"_id": self.author_id})

    @property
    def author_username(self) -> str:
        return self.author.username

    def telegram_text(self) -> str:
        answer_link = f"{self.base_uri()}/#/questions/{self.question_human_readable_id}?" \
                      f"answer={self.answer_id}&dismiss={self._id}"
        return f"Your question *{self.question_title}* got a new [answer]({answer_link}) by *{self.author_username}*"

    def icq_text(self) -> str:
        answer_link = f"{self.base_uri()}/#/questions/{self.question_human_readable_id}?" \
                      f"answer={self.answer_id}&dismiss={self._id}"
        return f"Your question '{self.question_title}' got a new answer by {self.author_username}: {answer_link}"


class PostNewCommentEvent(Event):

    SUBMODEL = "post_new_comment_event"

    API_FIELDS = (
        "post_id",
        "post_type",
        "root_id",
        "title",
        "comment_id",
        "author_username"
    )

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

    @property
    def author_username(self) -> str:
        return self.author.username

    @property
    def title(self) -> Optional[str]:
        if self.post.type == "question":
            return self.post.title
        return None

    @property
    def root_id(self):
        if self.post.type == "question":
            return self.post.human_readable_id
        else:
            return self.post.question.human_readable_id

    def telegram_text(self) -> str:
        comment_link = f"{self.base_uri()}/#/questions/{self.root_id}?comment={self.comment_id}&dismiss={self._id}"
        return f"You got a new [comment]({comment_link}) by *{self.author_username}*"

    def icq_text(self) -> str:
        comment_link = f"{self.base_uri()}/#/questions/{self.root_id}?comment={self.comment_id}&dismiss={self._id}"
        return f"You got a new comment by {self.author_username}: {comment_link}"


class MentionEvent(Event):

    SUBMODEL = "mention_event"

    API_FIELDS = (
        "post_id",
        "post_type",
        "root_id",
        "author_username"
    )

    post_id: ObjectIdField(required=True, rejected=True)
    post_type: StringField(required=True, rejected=True)
    author_id: ObjectIdField(required=True, rejected=True)

    @property
    def post(self) -> 'BasePost':
        return BasePost.find_one({"_id": self.post_id})

    @property
    def author(self) -> 'User':
        return User.find_one({"_id": self.author_id})

    @property
    def author_username(self) -> str:
        return self.author.username

    @property
    def root_id(self):
        if self.post_type == "question":
            root = self.post
        elif self.post_type == "answer":
            root = self.post.question
        else:
            parent = self.post.parent
            if parent.type == "question":
                root = parent
            else:
                root = parent.question
        return root.human_readable_id

    def telegram_text(self) -> str:
        post_link = f"{self.base_uri()}/#/questions/{self.root_id}"
        text = "You were mentioned in ["
        if self.post_type == "question":
            post_link += f"?dismiss={self._id}"
            text += "a question"
        elif self.post_type == "answer":
            post_link += f"?answer={self.post_id}&dismiss={self._id}"
            text += "an answer"
        else:
            post_link += f"?comment={self.post_id}&dismiss={self._id}"
            text += "a comment"
        text += f"]({post_link}) by *{self.author_username}*"
        return text

    def icq_text(self) -> str:
        post_link = f"{self.base_uri()}/#/questions/{self.root_id}"
        text = "You were mentioned in "
        if self.post_type == "question":
            post_link += f"?dismiss={self._id}"
            text += "a question"
        elif self.post_type == "answer":
            post_link += f"?answer={self.post_id}&dismiss={self._id}"
            text += "an answer"
        else:
            post_link += f"?comment={self.post_id}&dismiss={self._id}"
            text += "a comment"
        text += f" by {self.author_username}: {post_link}"
        return text


class AnswerAcceptedEvent(Event):

    SUBMODEL = "answer_accepted_event"

    API_FIELDS = (
        "question_id",
        "answer_id",
        "accepted_by_username",
    )

    answer_id: ObjectIdField(required=True, rejected=True)
    accepted_by_id: ObjectIdField(required=True, rejected=True)

    @property
    def answer(self) -> 'Answer':
        return Answer.find_one({"_id": self.answer_id})

    @property
    def accepted_by(self) -> 'User':
        return User.find_one({"_id": self.accepted_by_id})

    @property
    def accepted_by_username(self) -> str:
        return self.accepted_by.username

    @property
    def question_id(self):
        return self.answer.question.human_readable_id

    def telegram_text(self) -> str:
        answer_link = f"{self.base_uri()}/#/questions/{self.question_id}?answer={self.answer_id}&dismiss={self._id}"
        return f"Your [answer]({answer_link}) to question *{self.answer.question.title}* was " \
               f"accepted by *{self.accepted_by_username}*"

    def icq_text(self) -> str:
        answer_link = f"{self.base_uri()}/#/questions/{self.question_id}?answer={self.answer_id}&dismiss={self._id}"
        return f"Your answer to question '{self.answer.question.title}' was " \
               f"accepted by {self.accepted_by_username}: {answer_link}"


Event.register_submodel(TagNewQuestionEvent.SUBMODEL, TagNewQuestionEvent)
Event.register_submodel(QuestionNewAnswerEvent.SUBMODEL, QuestionNewAnswerEvent)
Event.register_submodel(PostNewCommentEvent.SUBMODEL, PostNewCommentEvent)
Event.register_submodel(MentionEvent.SUBMODEL, MentionEvent)
Event.register_submodel(AnswerAcceptedEvent.SUBMODEL, AnswerAcceptedEvent)


from .user import User
from .post import Question, BasePost, Answer, Comment
