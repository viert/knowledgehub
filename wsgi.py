import os
from cachelib import SimpleCache
from uengine.context import ctx
from ask import app, force_init_app

force_init_app()

if isinstance(ctx.cache, SimpleCache):
    if not os.getenv("UENGINE_USE_SIMPLE_CACHE"):
        raise RuntimeError("""Running your application under uwsgi control without centralized cache
is dangerous. If you rely on cache invalidation your app instances will be
able to invalidate their own in-memory cache while others will consider the
same cache keys still valid.

If you're sure it's OK for your project please set:
 
UENGINE_USE_SIMPLE_CACHE=1

""")

app_callable = app.flask