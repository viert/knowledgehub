from bot.bot import Bot
from .abstract_bot import AbstractBot
from glasskit import ctx
from glasskit import json


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
                print(response)
                if "events" not in response:
                    ctx.log.error("no events field in response")
                    continue
                for event in response["events"]:
                    event_id = event["eventId"]
                    self.process_event(event)

        except KeyboardInterrupt:
            ctx.log.info("SIGINT received, about to quit")
            self.poller.stopped = True

    def process_event(self, event):
        if event["type"] != "newMessage":
            ctx.log.debug("unknown event type '%s', skipping %s", event["type"], event)
            return

        chat = event["payload"]["chat"]
        if chat["type"] != "private":
            self.send_message(chat["chatId"], "Hey there! Unfortunately I'm not capable of working in groups. "
                                              "Please add me privately")
            return

        from pprint import pprint
        pprint(event)
