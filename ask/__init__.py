import os

from lazy_object_proxy import Proxy
from uengine.base import Base
from uengine import ctx

from ask.errors import ConfigurationError
from ask.controllers.main import gen_main_ctrl
from ask.controllers.api.v1.account import account_ctrl
from ask.controllers.api.v1.questions import questions_ctrl
from ask.controllers.api.v1.users import users_ctrl


def get_version():
    cur_dir = os.path.dirname(__file__)
    version_file = os.path.join(cur_dir, '__version__')
    if os.path.exists(version_file):
        return open(version_file).read().strip()

    return "development"


class App(Base):

    VERSION = get_version()

    def configure_routes(self):
        ctx.log.info("Configuring endpoints")

        endpoints = [
            {"prefix": "", "ctrl": gen_main_ctrl(self), "name": "main"},
            {"prefix": "/api/v1/account", "ctrl": account_ctrl, "name": "account"},
            {"prefix": "/api/v1/users", "ctrl": users_ctrl, "name": "users"},
            {"prefix": "/api/v1/questions", "ctrl": questions_ctrl, "name": "questions"},
        ]

        for ep in endpoints:
            ctx.log.debug("Controller[%s] @ %s/", ep["name"], ep["prefix"])
            self.flask.register_blueprint(ep["ctrl"], url_prefix=ep["prefix"])

    def setup_oauth(self):
        from ask.idconnect.config import get_conf
        from ask.idconnect.facebook import FacebookProvider
        from ask.idconnect.yandex import YandexProvider
        FacebookProvider().register()
        YandexProvider().register()

    def after_configured(self):
        if "base_uri" not in ctx.cfg:
            raise ConfigurationError("base_uri is missing from configuration")
        self.setup_oauth()


def force_init_app():
    _ = app.__doc__  # Doing anything with the app triggers Proxy and creates the real object


app = Proxy(App)