from commands import Command
from ask import app


class Run(Command):
    def run(self):
        app.run(debug=True)