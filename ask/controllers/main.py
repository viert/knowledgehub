import flask

from glasskit import ctx
from glasskit.cache import check_cache
from glasskit.api import json_response
from .auth_controller import AuthController


def gen_main_ctrl(app):
    main_ctrl = AuthController("main", __name__, require_auth=False)

    def index():
        routes = []
        for rule in app.flask.url_map.iter_rules():
            routes.append({
                "endpoint": rule.endpoint,
                "route": rule.rule,
                "methods": rule.methods
            })
        return json_response({"routes": routes})

    def app_info():
        results = dict(
            app={"name": "Knowledge Hub", "version": app.version},
            mongodb=ctx.db.mongodb_info(),
            cache={"type": ctx.cache.__class__.__name__, "active": check_cache()},
            flask_version=flask.__version__
        )

        for shard_id, shard in ctx.db.shards.items():
            results["mongodb"]["shards"][shard_id] = shard.conn.client.server_info()

        return json_response({"app_info": results})

    main_ctrl.route("/")(index)
    main_ctrl.route("/app_info")(app_info)

    return main_ctrl
