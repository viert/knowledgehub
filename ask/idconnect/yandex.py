import requests
from flask import json
from uengine import ctx
from .provider import BaseProvider
from ask.errors import OAuthError


class YandexProvider(BaseProvider):

    PROVIDER_NAME = "yandex"

    def authorize_uri(self, state):
        if type(state) != str:
            state = json.dumps(state)
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&state={state}"

    def acquire_token(self, code):
        uri = "https://oauth.yandex.ru/token"
        payload = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        ctx.log.debug("about to perform token request via %s", uri)
        resp = requests.post(uri, payload)
        if resp.status_code != 200:
            raise OAuthError("non-successful status code from oauth provider access_token handler", payload={"status_code": resp.status_code})
        data = resp.json()

        if "access_token" not in data:
            raise OAuthError("access_token is not in response data")
        return data["access_token"]

    def get_user_data(self, token):
        uri = "https://login.yandex.ru/info?format=json"
        headers = {"Authorization": f"OAuth {token}"}
        resp = requests.get(uri, headers=headers)
        if resp.status_code != 200:
            raise OAuthError("non-successful status code from oauth provider userdata handler", payload={"status_code": resp.status_code})
        attrs = resp.json()
        print(attrs)
        return {
            "ext_id": f"yandex_{attrs['id']}",
            "username": attrs["display_name"],
            "first_name": attrs["first_name"],
            "last_name": attrs["last_name"],
        }
