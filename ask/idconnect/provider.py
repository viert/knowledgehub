from glasskit import ctx
from .config import get_conf


class BaseProvider:

    PROVIDER_NAME = None
    PROVIDER_MAP = {}
    state = None

    def __init__(self):
        if self.PROVIDER_NAME is None:
            raise RuntimeError("can't instantiate BaseProvider abstract class")
        cfg = get_conf(self.PROVIDER_NAME)
        if cfg is None:
            raise RuntimeError(f"no configuration for provider {self.PROVIDER_NAME} given")
        self.client_id = cfg[0]
        self.client_secret = cfg[1]
        self.redirect_uri = cfg[2]
        self.extra = cfg[3]

    def authorize_uri(self, state):
        raise NotImplementedError("authorize_uri method must be overriden")

    def acquire_token(self, code):
        raise NotImplementedError("acquire_token method must be overriden")

    def get_user_data(self, token):
        raise NotImplementedError("_fetch_user_data method must be overriden")

    def register(self):
        if self.PROVIDER_NAME is None:
            raise RuntimeError(f"error registering {self.__class__.__name__} provider: PROVIDER_NAME is not defined")
        BaseProvider.PROVIDER_MAP[self.PROVIDER_NAME] = self
        ctx.log.info(f"OAuth2 provider \"{self.PROVIDER_NAME}\" registered")

    @classmethod
    def get_provider(cls, provider_name):
        if provider_name not in cls.PROVIDER_MAP:
            raise RuntimeError(f"provider {provider_name} not found or not registered")
        return cls.PROVIDER_MAP[provider_name]

    def provider_info(self):
        return {
            "provider_name": self.PROVIDER_NAME,
            "authorize_uri": self.authorize_uri(state=self.PROVIDER_NAME),
            **self.extra
        }

    @classmethod
    def list_provider_info(cls):
        return [p.provider_info() for p in cls.PROVIDER_MAP.values()]
