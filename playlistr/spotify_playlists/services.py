import requests as requests

from spotify_playlists import models
from urllib.parse import urlencode
from base64 import b64encode


class API:
    def __init__(self, client_id, client_secret, scope, redirect_uri):
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._redirect_uri = redirect_uri

    def get_auth_request_url(self):
        data = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
            "scope": self._scope,
        }
        return "https://accounts.spotify.com/authorize?" + urlencode(data)

    def update_user_token(self, user):
        if isinstance(user, models.User):
            data = {
                "grant_type": "refresh_code",
                "refresh_token": user.refresh_token,
            }
            headers = {
                "Authorization": "Basic " + b64encode(bytes(self._client_id + ":" + self._client_secret))
            }
            r = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
            return r
        else:
            raise TypeError("user must be an instance of models.User")
