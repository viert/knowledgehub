from glasskit.queue import BaseTask


class NewPostTask(BaseTask):

    TYPE = "NEW_POST_TASK"

    @classmethod
    def create(cls, post_id):
        return cls({
            "post_id": post_id
        })

    @property
    def post_id(self):
        return self.data["post_id"]


NewPostTask.register()
