from glasskit import ctx
from glasskit.queue import BaseWorker
from glasskit.queue.task import BaseTask

from ask.models.post import BasePost

from .sync_tags_task import SyncTagsTask
from .post_indexer_task import PostIndexerTask


class Worker(BaseWorker):

    def run_task(self, task: BaseTask):
        if isinstance(task, SyncTagsTask):
            self.rt_sync_tags(task)
        elif isinstance(task, PostIndexerTask):
            self.rt_post_indexer(task)
        else:
            ctx.log.error("task type %s is not supported", task.TYPE)

    @staticmethod
    def rt_sync_tags(task: SyncTagsTask):
        from ask.models import Tag
        Tag.sync(task.tags)
        ctx.log.info("tags %s synced", task.tags)

    @staticmethod
    def rt_post_indexer(task: PostIndexerTask):
        if task.delete:
            ctx.es.delete(index="posts", id=task.post_id)
        else:
            post: BasePost = BasePost.get(task.post_id)
            if post is None:
                ctx.log.error("error indexing post %s: post not found", task.post_id)
                return
            doc = post.get_indexer_document()
            ctx.es.index(index="posts", id=task.post_id, body=doc)
