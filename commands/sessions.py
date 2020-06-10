from uengine import ctx
from commands import Command
from datetime import datetime


class Sessions(Command):

    def init_argument_parser(self, parser):
        parser.add_argument("action", type=str, nargs=1,
                            choices=["cleanup", "count"])

    def run(self):

        action = self.args.action[0]
        if action == "count":
            total = ctx.db.meta.ro_conn["sessions"].find().count()
            expired = ctx.db.meta.ro_conn["sessions"].find(
                {"expiration": {"$lt": datetime.now()}}).count()
            print(f"Total number of sessions: {total}, expired: {expired}")
            if expired > 0:
                print("Use <micro.py sessions cleanup> to remove old sessions manually")

        elif action == "cleanup":
            print("Starting sessions clean up process...")
            count = ctx.db.meta.cleanup_sessions()
            if count == 0:
                print("There's no expired sessions to clean up")
            else:
                print(f"{count} expired sessions have been cleaned up")