from glasskit import ctx
from telegram.bot import Bot
from telegram.error import TimedOut, TelegramError
from telegram.parsemode import ParseMode

from ask.models import User, Chat
from .abstract_bot import AbstractBot


class TelegramBot(AbstractBot):

    NETWORK_NAME = "telegram"
    NETWORK_BASE_URL = "https://api.telegram.org/bot"

    def __init__(self):
        super(TelegramBot, self).__init__()
        self.bot = Bot(token=self.token, base_url=self.base_url)

    def start(self):
        self.poller.start()
        me = self.bot.getMe()
        ctx.log.info("starting telegram bot %s", me)
        offset = None
        try:
            while True:
                try:
                    updates = self.bot.get_updates(timeout=60, offset=offset)
                except TimedOut:
                    continue
                except TelegramError as e:
                    ctx.log.error("telegram error while getting updates: %s", e)
                    continue

                for update in updates:
                    offset = update.update_id + 1
                    try:
                        self.process_update(update)
                    except Exception as e:
                        ctx.log.exception("Could not process Telegram update: %s Ignoring", e)

        except KeyboardInterrupt:
            ctx.log.info("SIGINT received, exiting")
            self.poller.stopped = True
            self.poller.join()

    def send_message(self, where: str, what: str):
        self.bot.send_message(where, what, parse_mode=ParseMode.MARKDOWN)

    def process_update(self, update):
        message = update.message
        if message is None:
            message = update.edited_message
            if message is None:
                ctx.log.debug("update %s has no message", update.to_dict())
                return

        if message.entities:
            for entity in message.entities:
                if entity.type == 'bot_command':
                    cmd = message.text[entity.offset:entity.offset + entity.length]
                    method_name = f"cmd_{cmd[1:]}"
                    if not hasattr(self, method_name):
                        ctx.log.debug("unknown command '%s' from chat %s",
                                      method_name, message.chat.to_dict())
                        return
                    method = getattr(self, method_name)
                    method(message)
        else:
            self.process_message(message)

    def process_message(self, message):
        pass

    def cmd_start(self, message):
        ctx.log.debug("running command 'start' by request from %s", message.chat.to_dict())
        if message.chat.type != "private":
            self.send_message(message.chat.id, "Hey there! Unfortunately I'm not capable of working in groups. "
                                               "Please add me privately")
            return
        chat = Chat.find_one({"chat_id": message.chat.id})
        if chat is None:
            user = User.find_by_telegram_id(message.chat.username)
            if user is None:
                return self._new_user_message(message)

            chat = Chat({
                "chat_id": message.chat.id,
                "user_id": user._id,
                "network_type": "telegram"
            })
            chat.save()
            return self._new_user_confirmed_message(message)

    def cmd_stop(self, message):
        chat = Chat.find_one({"chat_id": message.chat.id})
        if chat is not None:
            chat.destroy()
            return self._user_stop_message(message)

    def cmd_ping(self, message):
        ctx.log.debug("running command 'ping' by request from %s", message.chat.to_dict())
        chat = Chat.find_one({"chat_id": message.chat.id})
        if chat is None:
            return
        self.send_message(message.chat.id, "pong")

    def _new_user_message(self, message):
        base_url = ctx.cfg.get("base_url", "http://localhost:8000")
        link = f"{base_url}/#/profile"
        text = "Hey there, I'm a KnowledgeHub bot. You may have forgotten to " \
               "fill in your telegram id on your profile page. Or may have misspelled it. " \
               "A typo or something, a common thing, no worries. Well, you have two options " \
               "of fixing that. The first one is broken and the second one is to fill in " \
               "your telegram id on [profile page]({link}) properly and run /start once again. " \
               "I'll be waiting right here. Not going anywhere. Honestly."
        self.send_message(message.chat.id, text.format(link=link))

    def _new_user_confirmed_message(self, message):
        self.send_message(message.chat.id, "Hey there, I'm a KnowledgeHub bot. Looks, like you "
                                           "did it all right, I have found your account and connected "
                                           "it to this chat. Here's where your notifications will go to. "
                                           "If you're fed up, this chat can be muted. Or just type /stop "
                                           "and the nightmare is over. But remember that I'll forget you "
                                           "in that case. Forever. Well, at least until you type /start once again.")

    def _user_stop_message(self, message):
        self.send_message(message.chat.id, "Bye! It's a pity we couldn't settle. If you "
                                           "change your mind, I'm always here. Just type in "
                                           "/start and we'll try to start from scratch")
