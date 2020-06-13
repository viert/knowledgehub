from commands import Command
from ask.tasks.worker import Worker


class Tasks(Command):

    def run(self):
        wrk = Worker()
        wrk.process_tasks()
