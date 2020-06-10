documents_per_page = 10
app_secret_key = "_some_secret_key_"

flask_settings = {
    "SESSION_COOKIE_NAME": "_ask_session_id"
}

session_expiration_time = 86400 * 7 * 2  # 2 weeks
token_expiration_time = 86400 * 7 * 2  # 2 weeks

# If token_auto_prolongation is True, the token lifetime is calculated since updated_at which is updated
# every time user is authorized with the token.
#
# Otherwise it's calculated since created_at, therefore tokens live exactly `token_expiration_time` seconds
token_auto_prolongation = True

pymongo_extra = {
    "serverSelectionTimeoutMS": 1100,
    "socketTimeoutMS": 1100,
    "connectTimeoutMS": 1100,
}

database = {
    "meta": {
        "uri": "mongodb://localhost",
        "pymongo_extra": pymongo_extra,
        "dbname": "ask_prod",
    },
    "shards": {}
}

log_level = "info"
log_format = "[%(asctime)s] %(levelname)s\t%(module)-8.8s:%(lineno)-3d %(request_id)-8s %(message)s"
debug = False