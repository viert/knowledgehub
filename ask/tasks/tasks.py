from uengine.queue.task import BaseTask


class SyncTagsTask(BaseTask):

    TYPE = "SYNC_TAGS"

    @classmethod
    def create(cls, tags):
        return SyncTagsTask({"tags": tags})

    @property
    def tags(self):
        return self.data["tags"]


SyncTagsTask.register()
