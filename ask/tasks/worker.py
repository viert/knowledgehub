from uengine import ctx
from uengine.queue import BaseWorker


class Worker(BaseWorker):

    def run_task(self, task):
        if task.TYPE == "SYNC_TAGS":
            self.rt_sync_tags(task)
        else:
            ctx.log.error("task type %s is not supported", task.TYPE)

    @staticmethod
    def rt_sync_tags(task):
        from ask.models import Tag
        Tag.sync(task.tags)
        ctx.log.info("tags %s synced", task.tags)
