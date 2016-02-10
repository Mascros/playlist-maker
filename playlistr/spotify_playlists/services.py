import requests as requests
import json
from spotify_playlists import models
from urllib.parse import urlencode
from base64 import b64encode
from datetime import datetime, timedelta


class API:
    def __init__(self, client_id, client_secret, scope, redirect_uri):
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._redirect_uri = redirect_uri
        self._auth = "Basic %s" % b64encode(str(self._client_id + ":" + self._client_secret).encode()).decode()

    def get_auth_request_url(self):
        data = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
            "scope": self._scope,
        }
        return "https://accounts.spotify.com/authorize?" + urlencode(data)

    def get_login_tokens(self, code):
        """
        Get the login tokens and their expiry details for a given user auth code.
        :param code: Str - The code returned by spotify
        :return: Dict - The access and refresh tokens as str, access token expiry as datetime
        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self._redirect_uri
        }
        headers = {
            "Authorization": self._auth
        }
        r = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
        body = json.loads(r.text)
        expiry = datetime.now() + timedelta(seconds=body['expires_in']-2)  # -2 to be safe, as time will have passed
        result = {
            "access_token": body['access_token'],
            "refresh_token": body['refresh_token'],
            "expiry": expiry
        }
        return result

    def update_user_token(self, user):
        if isinstance(user, models.User):
            data = {
                "grant_type": "refresh_code",
                "refresh_token": user.refresh_token
            }
            headers = {
                "Authorization": self._auth
            }
            r = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
            raise NotImplementedError("Not finished")
        else:
            raise TypeError("user must be an instance of models.User")
