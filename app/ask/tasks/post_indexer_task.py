from typing import Union
from bson import ObjectId
from glasskit.queue import BaseTask


class PostIndexerTask(BaseTask):

    TYPE = "POST_INDEXER_TASK"

    @classmethod
    def create(cls, post_id: Union[ObjectId, str], delete: bool = False):
        return cls({
            "post_id": post_id,
            "delete": delete,
        })

    @property
    def post_id(self) -> Union[ObjectId, str]:
        return self.data["post_id"]

    @property
    def delete(self) -> bool:
        return self.data["delete"]


PostIndexerTask.register()
