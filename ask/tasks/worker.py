from glasskit import ctx
from glasskit.queue import BaseWorker
from glasskit.queue.task import BaseTask
from .sync_tags_task import SyncTagsTask


class Worker(BaseWorker):

    def run_task(self, task: BaseTask):
        if isinstance(task, SyncTagsTask):
            self.rt_sync_tags(task)
        else:
            ctx.log.error("task type %s is not supported", task.TYPE)

    @staticmethod
    def rt_sync_tags(task: SyncTagsTask):
        from ask.models import Tag
        Tag.sync(task.tags)
        ctx.log.info("tags %s synced", task.tags)
