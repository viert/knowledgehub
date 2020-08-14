import requests
from glasskit import ctx, json

from .provider import BaseProvider
from ask.errors import OAuthError


class FacebookProvider(BaseProvider):

    PROVIDER_NAME = "facebook"

    def authorize_uri(self, state):
        if type(state) != str:
            state = json.dumps(state)
        return f"https://www.facebook.com/v7.0/dialog/oauth?client_id={self.client_id}" \
               f"&redirect_uri={self.redirect_uri}&state={state}"

    def acquire_token(self, code):
        uri = f"https://graph.facebook.com/v7.0/oauth/access_token?" \
              f"client_id={self.client_id}&client_secret={self.client_secret}" \
              f"&redirect_uri={self.redirect_uri}&code={code}"
        ctx.log.debug("about to perform token request via %s", uri)
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise OAuthError("non-successful status code from oauth provider access_token handler", payload={"status_code": resp.status_code})
        data = resp.json()
        if "access_token" not in data:
            raise OAuthError("access_token is not in response data")
        return data["access_token"]

    def get_user_data(self, token):
        uri = f"https://graph.facebook.com/v7.0/me?fields=first_name,last_name,id&access_token={token}"
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise OAuthError("non-successful status code from oauth provider userdata handler", payload={"status_code": resp.status_code})
        attrs = resp.json()
        return {
            "ext_id": f"fb_{attrs['id']}",
            "username": f"fb_{attrs['id']}",
            "first_name": attrs["first_name"],
            "last_name": attrs["last_name"],
        }
