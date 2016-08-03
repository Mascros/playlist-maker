import requests as requests
import json
from spotify_playlists import models
from urllib.parse import urlencode
from base64 import b64encode
from datetime import datetime, timedelta
from os import path


class SpotifyAPI:
    def __init__(self):
        module_dir = path.dirname(__file__)
        file_path = path.join(module_dir, "secret.txt")
        f = open(file_path, "r")
        client_secret = f.readline()
        f.close()

        self._client_id = "38c7aa7c8b0a4172aa46a5b7833b8454"
        self._client_secret = client_secret
        self._scope = ("user-read-private user-read-email user-library-read "
                       "playlist-modify-public playlist-modify-private")
        self._redirect_uri = "http://127.0.0.1:8000/redirect"
        self._auth = "Basic %s" % b64encode(str(self._client_id + ":" + self._client_secret).encode()).decode()

    def get_auth_request_url(self):
        """
        Get the url for the user to click to log in with Spotify
        :return: Str - The url
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

        expiry = datetime.now() + timedelta(seconds=body['expires_in'] - 2)
        # -2 to be safe, as time will have passed

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
        :return: Dict - The data returned by the SpotifyAPI
        """
        headers = {
            "Authorization": "Bearer " + access_token
        }
        r = requests.get("https://api.spotify.com/v1/me", headers=headers)
        return json.loads(r.text)

    @staticmethod
    def get_user_saved_tracks(access_token):
        """
        Get the tracks the user has saved
        :param access_token: up to date access token for the user
        :return: list of the users saved tracks
        """
        headers = {
            "Authorization": "Bearer " + access_token
        }
        url = "https://api.spotify.com/v1/me/tracks"
        tracks = []
        while url is not None:
            # while there are tracks still to be fetched
            r = json.loads(requests.get(url, headers=headers).text)

            # add tracks to list
            tracks.append(r.items)

            # r.next has the url for the next (up to 20) tracks.
            # If there are no tracks r.next is None
            url = r.next

        return tracks

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
            user.token_expiry = datetime.now() + timedelta(seconds=r['expires_in'] - 2)
            user.save()
        else:
            raise TypeError("user must be an instance of models.User")

    @staticmethod
    def create_playlist(user_id, access_token, name):
        """
        Create a playlists in the users spotify account
        :param user_id: The id for the user
        :param access_token: A valid access token for the user
        :param name: The name of the playlist
        :return: The playlist ID
        """
        url = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "public": True
        }
        r = json.loads(requests.post(url, headers=headers, data=data).text)
        return r['id']

    @staticmethod
    def _track_ids_to_uri_csv(track_ids):
        """
        Takes a list of Track IDs and returns a CSV string of track URIs
        :param track_ids: list of track ids
        :return: CSV str of URIs for the tracks
        """
        uri_csv = ""
        for id in track_ids:
            uri_csv += "spotify:track:{},".format(id)

        # remove the final comma so that its valid CSV
        uri_csv.rstrip(",")
        return uri_csv

    def add_tracks_to_playlist(self, user_id, access_token, playlist_id, track_ids):
        """
        Add the given tracks to the playlist of the given user
        :param user_id: ID of the user to whom the playlist belongs
        :param access_token: A valid access token for the user
        :param playlist_id: ID of the playlist to which the tracks should be added
        :param track_ids: A list of track IDs to be added to the playlist. Max 100
        """
        url = "https://api.spotify.com/v1/users/{}/playlists/{}/tracks".format(user_id, playlist_id)
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        data = {
            "uris": self._track_ids_to_uri_csv(track_ids)
        }
        requests.post(url, headers=headers, data=data)
