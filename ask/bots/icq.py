import re
from typing import List
from bot.bot import Bot


from .abstract_bot import AbstractBot
from ask.models import Chat, User
from glasskit import ctx


CMD_MATCH = re.compile(r'(?:\A|\s)\/(\w+)\b')


class ICQBot(AbstractBot):

    NETWORK_NAME = "icq"
    NETWORK_BASE_URL = "https://api.icq.net/bot/v1"

    def __init__(self):
        super(ICQBot, self).__init__()
        self.bot = Bot(token=self.token, api_url_base=self.base_url)

    def send_message(self, where: str, what: str):
        self.bot.send_text(where, what)

    def start(self):
        self.poller.start()
        event_id = None
        try:
            while True:
                try:
                    response = self.bot.events_get(last_event_id=event_id)
                except Exception as e:
                    ctx.log.error("error receiving icq events: %s", e)
                    continue
                response = response.json()

                if "events" not in response:
                    ctx.log.error("no events field in response")
                    continue
                for event in response["events"]:
                    event_id = event["eventId"]
                    self.process_event(event)

        except KeyboardInterrupt:
            ctx.log.info("SIGINT received, about to quit")
            self.poller.stopped = True

    def _new_user_message(self, event):
        base_url = ctx.cfg.get("base_uri", "http://localhost:8000/")
        link = f"{base_url}#/profile"
        text = "Hey there, I'm a KnowledgeHub bot. You may have forgotten to " \
               "fill in your ICQ id on your profile page. Or may have misspelled it. " \
               "A typo or something, a common thing, no worries. Well, you have two options " \
               "of fixing that. The first one is broken and the second one is to fill in " \
               "your ICQ id on profile page: {link} properly and run /start once again. " \
               "I'll be waiting right here. Not going anywhere. Honestly."
        self.send_message(event["payload"]["chat"]["chatId"], text.format(link=link))

    def _new_user_confirmed_message(self, event):
        text = "Hey there, I'm a KnowledgeHub bot. Looks, like you " \
               "did it all right, I have found your account and connected " \
               "it to this chat. Here's where your notifications will go to. " \
               "If you're fed up, this chat can be muted. Or just type /stop " \
               "and the nightmare is over. But remember that I'll forget you " \
               "in that case. Forever. Well, at least until you type /start once again."
        self.send_message(event["payload"]["chat"]["chatId"], text)

    @staticmethod
    def search_for_commands(text: str) -> List[str]:
        return CMD_MATCH.findall(text)

    def process_event(self, event):
        if event["type"] != "newMessage":
            ctx.log.debug("unknown event type '%s', skipping %s", event["type"], event)
            return

        commands = self.search_for_commands(event["payload"]["text"])
        for cmd in commands:
            method_name = f"cmd_{cmd}"
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                method(event)

    def cmd_start(self, event):
        chat_dsc = event["payload"]["chat"]
        ctx.log.debug("running command 'start' by request from %s", chat_dsc)

        if chat_dsc["type"] != "private":
            self.send_message(chat_dsc["chatId"], "Hey there! Unfortunately I'm not capable of working in groups. "
                                              "Please add me privately")
            return

        chat = Chat.find_one({"chat_id": chat_dsc["chatId"], "network_type": "icq"})
        if chat is None:
            user = User.find_by_icq_id(event["payload"]["from"]["userId"])
            if user is None:
                return self._new_user_message(event)

            chat = Chat({
                "chat_id": chat_dsc["chatId"],
                "user_id": user._id,
                "network_type": "icq"
            })
            chat.save()
            return self._new_user_confirmed_message(event)

    def cmd_ping(self, event):
        ctx.log.debug("running command 'ping' by request from %s", event["payload"]["chat"])
        chat = Chat.find_one({"chat_id": event["payload"]["chat"]["chatId"]})
        if chat is None:
            return
        self.send_message(chat.chat_id, "pong")

    def cmd_stop(self, event):
        ctx.log.debug("running command 'stop' by request from %s", event["payload"]["chat"])
        chat = Chat.find_one({"chat_id": event["payload"]["chat"]["chatId"]})
        if chat is not None:
            chat.destroy()
