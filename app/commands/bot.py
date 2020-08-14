from glasskit.commands import Command
from ask.bots.telegram import TelegramBot
from ask.bots.icq import ICQBot
from ask import force_init_app


class Bot(Command):

    def init_argument_parser(self, parser):
        parser.add_argument("bot_type", nargs=1, choices=["telegram", "icq"])

    def run(self):
        force_init_app()
        bot_type = self.args.bot_type[0]
        if bot_type == "telegram":
            bot = TelegramBot()
            bot.start()
        elif bot_type == "icq":
            bot = ICQBot()
            bot.start()
