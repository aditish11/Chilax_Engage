import json
import requests
from urllib.parse import quote


class SpotifyClient:
    #API URLS for Spotify
    API_VERSION = "v1"
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

    #Setting the scope from server's side
    STATE = ""
    SHOW_DIALOG_bool = True
    SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
    SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private user-read-recently-played"

    # URL for Client side
    CLIENT_SIDE_URL = 'http://localhost:8002/callback'

    def __init__(self, client_id, client_secret, client_side_url=CLIENT_SIDE_URL, port=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_side_url = client_side_url
        self.port = port
        self._access_token = ''
        self.authorization_header = ''
        self.redirect_uri = self.client_side_url

    def get_auth_url(self):
        auth_query_parameters = {
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.SCOPE,
            "show_dialog": self.SHOW_DIALOG_str,
            "client_id": self.client_id
            # "state": STATE,
        }

        url_args = "&".join([f"{key}={quote(str(val))}" for key, val in auth_query_parameters.items()])
        return f"{self.SPOTIFY_AUTH_URL}/?{url_args}"

    def get_authorization(self, auth_token):
        """
        returning authorization data and setting the authorization_header
        :param auth_token:
        :return: dict
        """

        data = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        post_request = requests.post(self.SPOTIFY_TOKEN_URL, data=data)

        response_data = json.loads(post_request.text)
        self._access_token = response_data["access_token"]
        self.authorization_header = {"Authorization": f"Bearer {self._access_token}"}

        return dict(
            access_token=response_data["access_token"],
            refresh_token=response_data["refresh_token"],
            token_type=response_data["token_type"],
            expires_in=response_data["expires_in"],
        )
