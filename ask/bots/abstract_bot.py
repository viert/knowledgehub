from glasskit import ctx
from glasskit.errors import ConfigurationError


class AbstractBot:

    NETWORK_NAME = None
    NETWORK_BASE_URL = None

    def __init__(self):
        from .event_emitter import EventEmitter
        botcfg = ctx.cfg.get("bot")
        if not botcfg:
            raise ConfigurationError("no bot configuration section found")

        net_cfg = botcfg.get(self.NETWORK_NAME)
        if not net_cfg:
            raise ConfigurationError(f"no {self.NETWORK_NAME} configuration provided")

        self.token = net_cfg.get("token")
        self.base_url = net_cfg.get("base_url", self.NETWORK_BASE_URL)
        self.poller = EventEmitter(self, self.NETWORK_NAME)

    def send_message(self, where: str, what: str):
        raise NotImplementedError("abstract class")

    def start(self):
        raise NotImplementedError("abstract class")
