from commands import Command
from ask.tasks.worker import process_tasks


class Tasks(Command):

    def run(self):
        process_tasks()

