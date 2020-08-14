import requests
from urllib.parse import parse_qs
from glasskit import ctx, json

from .provider import BaseProvider
from ask.errors import OAuthError


class GithubProvider(BaseProvider):

    PROVIDER_NAME = "github"

    def authorize_uri(self, state):
        if type(state) != str:
            state = json.dumps(state)
        self.state = state
        return f"https://github.com/login/oauth/authorize?client_id={self.client_id}" \
               f"&redirect_uri={self.redirect_uri}&state={state}"

    def acquire_token(self, code):
        uri = f"https://github.com/login/oauth/access_token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
        }
        ctx.log.debug("about to perform token request via %s", uri)
        resp = requests.post(uri, json=payload)
        if resp.status_code != 200:
            raise OAuthError("non-successful status code from oauth provider access_token handler", payload={"status_code": resp.status_code})
        try:
            data = parse_qs(resp.content)
        except Exception as e:
            raise OAuthError(f"error parsing access token data from github {e}")
        if b"access_token" not in data:
            raise OAuthError("access_token is not in response data")
        return data[b"access_token"][0].decode()

    def get_user_data(self, token):
        uri = "https://api.github.com/user"
        headers = {"Authorization": f"token {token}"}
        resp = requests.get(uri, headers=headers)
        data = resp.json()

        first_name = None
        last_name = None
        name = data["name"].split()

        if name:
            first_name = name[0]
            last_name = " ".join(name[1:])

        return {
            "ext_id": f"gh_{data['id']}",
            "username": data["login"],
            "avatar_url": data["avatar_url"],
            "first_name": first_name,
            "last_name": last_name,
            "email": data["email"]
        }
