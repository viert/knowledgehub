from typing import Optional
from glasskit import ctx
from glasskit.queue import BaseWorker
from glasskit.queue.task import BaseTask

from ask.models.post import BasePost
from ask.utils import cut

from .sync_tags_task import SyncTagsTask
from .post_indexer_task import PostIndexerTask
from .new_post_task import NewPostTask


class Worker(BaseWorker):

    def run_task(self, task: BaseTask):
        if isinstance(task, SyncTagsTask):
            self.rt_sync_tags(task)
        elif isinstance(task, PostIndexerTask):
            self.rt_post_indexer(task)
        elif isinstance(task, NewPostTask):
            self.rt_new_post(task)
        else:
            ctx.log.error("task type %s is not supported", task.TYPE)

    @staticmethod
    def rt_sync_tags(task: SyncTagsTask):
        from ask.models import Tag
        Tag.sync(task.tags)
        ctx.log.info("tags %s synced", task.tags)

    @staticmethod
    def rt_post_indexer(task: PostIndexerTask):
        if not hasattr(ctx, "es"):
            ctx.log.error("elasticsearch is not configured, indexing skipped")
            return

        if task.delete:
            ctx.es.delete(index="posts", id=task.post_id)
            ctx.log.info("post %s has been deleted from index", task.post_id)
        else:
            post: BasePost = BasePost.get(task.post_id)
            if post is None:
                ctx.log.error("error indexing post %s: post not found", task.post_id)
                return
            doc = post.get_indexer_document()
            resp = ctx.es.index(index="posts", id=task.post_id, body=doc)
            if resp["result"] == "created":
                ctx.log.info("post %s has been indexed", task.post_id)
            elif resp["result"] == "updated":
                ctx.log.info("post %s index has been updated", task.post_id)

    @staticmethod
    def rt_new_post(task):
        post: Optional[BasePost] = BasePost.get(task.post_id)
        if not post:
            ctx.log.error("error processing new post %s: post not found", task.post_id)
            return
        ctx.log.info("generating events for a new post %s body='%s'", task.post_id, cut(post.body, max_len=50))
        post.generate_new_post_events()
