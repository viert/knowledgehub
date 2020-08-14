import os
import importlib
import inspect

from elasticsearch import Elasticsearch, TransportError, ImproperlyConfigured

from lazy_object_proxy import Proxy
from glasskit.base import Base
from glasskit import ctx

from ask.errors import ConfigurationError
from ask.search import MongoJSONSerializer

from ask.controllers.main import gen_main_ctrl
from ask.controllers.api.v1.account import account_ctrl
from ask.controllers.api.v1.questions import questions_ctrl
from ask.controllers.api.v1.users import users_ctrl
from ask.controllers.api.v1.subscriptions import subs_ctrl
from ask.controllers.api.v1.tags import tags_ctrl
from ask.controllers.api.v1.search import search_ctrl
from ask.controllers.api.v1.events import events_ctrl


def get_version():
    cur_dir = os.path.dirname(__file__)
    version_file = os.path.join(cur_dir, '__version__')
    if os.path.exists(version_file):
        return open(version_file).read().strip()

    return "development"


class App(Base):

    VERSION = get_version()

    def setup_controllers(self):
        ctx.log.info("Configuring controllers")

        endpoints = [
            {"prefix": "", "ctrl": gen_main_ctrl(self), "name": "main"},
            {"prefix": "/api/v1/account", "ctrl": account_ctrl, "name": "account"},
            {"prefix": "/api/v1/users", "ctrl": users_ctrl, "name": "users"},
            {"prefix": "/api/v1/tags", "ctrl": tags_ctrl, "name": "tags"},
            {"prefix": "/api/v1/questions", "ctrl": questions_ctrl, "name": "questions"},
            {"prefix": "/api/v1/subscriptions", "ctrl": subs_ctrl, "name": "subscriptions"},
            {"prefix": "/api/v1/search", "ctrl": search_ctrl, "name": "search"},
            {"prefix": "/api/v1/events", "ctrl": events_ctrl, "name": "events"},
        ]

        for ep in endpoints:
            ctx.log.debug("Controller[%s] @ %s/", ep["name"], ep["prefix"])
            self.flask.register_blueprint(ep["ctrl"], url_prefix=ep["prefix"])

    def setup_oauth(self):
        from ask.idconnect.config import get_conf
        from ask.idconnect.provider import BaseProvider

        providers = []
        idconnect_dir = os.path.join(self.app_dir, "idconnect")

        for filename in os.listdir(idconnect_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module_name = f"ask.idconnect.{module_name}"
                module = importlib.import_module(module_name)
                for obj_name in dir(module):
                    obj = getattr(module, obj_name)
                    if inspect.isclass(obj) and issubclass(obj, BaseProvider) and obj != BaseProvider:
                        providers.append(obj)

        for provider in providers:
            if get_conf(provider.PROVIDER_NAME):
                provider().register()
            else:
                ctx.log.info("Skipping OAuth2 provider %s, no configuration found", provider.PROVIDER_NAME)

    def setup_search(self):
        ctx.es = None
        ctx.log.info("Setting up Elasticsearch")

        search_cfg = ctx.cfg.get("search")
        if search_cfg is None:
            ctx.log.info("no search section found in config, elasticsearch will be disabled")
            return None
        nodes = search_cfg.get("nodes", [])
        options = search_cfg.get("options", {})
        try:
            ctx.es = Elasticsearch(nodes, serializer=MongoJSONSerializer(), **options)
        except (TransportError, ImproperlyConfigured) as e:
            ctx.log.error("error initializing elasticsearch driver: %s", e)

    def after_setup(self):
        if "base_uri" not in ctx.cfg:
            raise ConfigurationError("base_uri is missing from configuration")
        self.setup_oauth()
        self.setup_search()


def force_init_app():
    _ = app.__doc__  # Doing anything with the app triggers Proxy and creates the real object


app = Proxy(App)
