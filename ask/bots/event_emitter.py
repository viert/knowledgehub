from time import sleep
from threading import Thread
from glasskit import ctx
from ask.models.event import Event
from ask.models import User
from .abstract_bot import AbstractBot

DB_POLLER_PERIOD = 1  # seconds


class EventEmitter(Thread):

    def __init__(self, bot: 'AbstractBot', network_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stopped = False
        self.bot = bot
        self.network_type = network_type
        self.user_settings_field = f"notify_by_{self.network_type}"

    def send_event(self, user: 'User', event: 'Event'):
        chat = user.chat(self.network_type)
        if not chat:
            return
        text_getter = getattr(event, f"{self.network_type}_text")
        text = text_getter()
        ctx.log.info("about to send %s to %s", text, chat.chat_id)
        if text:
            self.bot.send_message(chat.chat_id, text)

    def process_event(self, event):
        ctx.log.info("processing event %s(%s)", event.__class__.__name__, event._id)
        user = event.user
        need_to_send = getattr(user, self.user_settings_field)
        if need_to_send:
            self.send_event(user, event)
        event.sent[self.network_type] = True
        event.save()

    def run(self) -> None:
        ctx.log.debug("%s bot db poller started", self.network_type)
        while not self.stopped:
            try:
                sleep(DB_POLLER_PERIOD)
                for event in Event.find_ready_to_send(self.network_type):
                    try:
                        self.process_event(event)
                    except Exception as e:
                        ctx.log.exception("Could not process event #%s in %s bot: %s",
                                          event._id, self.network_type, e)
            except KeyboardInterrupt:
                continue

        ctx.log.debug("%s bot db poller is exiting", self.network_type)
