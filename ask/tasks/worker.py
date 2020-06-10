from threading import Thread
from uengine import ctx
from time import sleep
from queue import Empty, Queue


def rt_sync_tags(task):
    from ask.models import Tag
    Tag.sync(task.tags)
    ctx.log.info("tags %s synced", task.tags)


def run_task(task):
    if task.TYPE == "SYNC_TAGS":
        rt_sync_tags(task)
    else:
        ctx.log.error("task type %s is not supported", task.TYPE)


class Worker(Thread):

    def __init__(self, q):
        super(Worker, self).__init__()
        self.stopped = False
        self.q = q

    def run(self) -> None:
        ctx.log.debug("Task-processing worker started")
        while not self.stopped:
            try:
                task = self.q.get(False)
                ctx.log.debug("Got task %s", task)
            except Empty:
                sleep(0.1)
                continue
            run_task(task)


def process_tasks(cnt=0):
    q = ctx.queue
    thq = Queue()
    wrk = Worker(thq)
    wrk.start()
    infinite = cnt == 0

    while True:
        try:
            for task in q.tasks:
                ctx.log.info("Received task %s", task)
                thq.put(task)
                if not infinite:
                    cnt -= 1
                    if cnt == 0:
                        break
        except KeyboardInterrupt:
            break
        except Exception as e:
            ctx.log.error("Error processing tasks: %s", e)

    wrk.stopped = True
