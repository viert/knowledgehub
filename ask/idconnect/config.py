from copy import copy
from glasskit import ctx
from ask.errors import ConfigurationError


def get_conf(provider_name):

    oacfg = ctx.cfg.get("oauth")
    if not oacfg:
        raise ConfigurationError("oauth is not configured")

    gcfg = oacfg.get("_global")

    if provider_name not in oacfg:
        ctx.log.error("no provider \"%s\" found", provider_name)
        return None

    provider_cfg = {
        **gcfg,
        **copy(oacfg[provider_name])
    }
    if "client_id" not in provider_cfg:
        raise ConfigurationError(f"oauth provider {provider_name} id field missing")
    if "client_secret" not in provider_cfg:
        raise ConfigurationError(f"oauth provider {provider_name} secret field missing")
    if "provider_name" not in provider_cfg:
        provider_cfg["provider_name"] = provider_name
    if "redirect_uri" not in provider_cfg:
        raise ConfigurationError(f"oauth provider {provider_name} redirect_uri field missing and no"
                                 f" global redirect_uri found")

    client_id = provider_cfg["client_id"]
    client_secret = provider_cfg["client_secret"]
    redirect_uri = provider_cfg["redirect_uri"]
    del provider_cfg["client_id"]
    del provider_cfg["client_secret"]
    del provider_cfg["redirect_uri"]

    return client_id, client_secret, redirect_uri, provider_cfg

