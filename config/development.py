documents_per_page = 10
app_secret_key = "_some_secret_key_"

flask_settings = {
    "SESSION_COOKIE_NAME": "_knowledgehub_session_id",
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SAMESITE": "Lax",
}

session_expiration_time = 86400 * 7 * 2  # 2 weeks
token_expiration_time = 86400 * 7 * 2  # 2 weeks
token_auto_prolongation = True

pymongo_extra = {
    "serverSelectionTimeoutMS": 1100,
    "socketTimeoutMS": 1100,
    "connectTimeoutMS": 1100,
}

database = {
    "meta": {
        "uri": "mongodb://localhost/ask_dev",
        "pymongo_extra": pymongo_extra,
    },
    "shards": {}
}

log_level = "debug"
log_format = "[%(asctime)s] %(levelname)s\t%(module)-8.8s:%(lineno)-3d %(request_id)-8s %(message)s"
debug = False

base_uri = "http://localhost:8080/"
oauth = {
    "_global": {
        "redirect_uri": "http://localhost:8080/api/v1/account/oauth_callback",
    },
    "facebook": {
        "client_id": "575364966512336",
        "client_secret": "62bab4f7f1d1b38ef79d5da9862d4873",
        "btn_class": "btn-primary",
        "fa_icon": "fab fa-facebook"
    },
    "yandex": {
        "client_id": "0082223625144c3794af7ac05d2701e1",
        "client_secret": "9f084bf8141d4a1fa94e92af39a4b4ea",
        "btn_class": "btn-yandex",
        "fa_icon": "fab fa-yandex"
    }
}
