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
        """
        Get the url for the user to click to log in with Spotify
        :return: Str- The url
        """
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
            "token_expiry": expiry
        }
        return result

    @staticmethod
    def get_current_user_profile(access_token):
        """
        Get the profile object for the current user
        :param access_token: the access_token for the user
        :return: Dict - The data returned by the API
        """
        headers = {
               "Authorization": "Bearer " + access_token
        }
        r = requests.get("https://api.spotify.com/v1/me", headers=headers)
        return json.loads(r.text)

    def update_user_token(self, user):
        """
        Update the access_token and token_expiry for a given user
        :param user: models.User - Will be mutated. Must have a refresh token
        :return: void
        """
        if isinstance(user, models.User):
            data = {
                "grant_type": "refresh_token",
                "refresh_token": user.refresh_token
            }
            headers = {
                "Authorization": self._auth
            }
            r = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
            r = json.loads(r.text)
            user.access_token = r['access_token']
            user.token_expiry = datetime.now() + timedelta(seconds=r['expires_in']-2)
            user.save()
        else:
            raise TypeError("user must be an instance of models.User")
