import base64
import json
import requests

class SpotifyOauth:

    def __init__(self) -> None:
        self.SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
        self.SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
        self.RESPONSE_TYPE = 'code'   
        self.HEADER = 'application/x-www-form-urlencoded'
        self.REFRESH_TOKEN = ''
        
    def getAuth(self, client_id, redirect_uri, scope) -> str:
        data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(self.SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
        return data

    def getToken(self, code, client_id, client_secret, redirect_uri) -> str:
        body = {
            "grant_type": 'authorization_code',
            "code" : code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }
            
        message = f"{client_id}:{client_secret}"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        headers = {"Content-Type" : self.HEADER, "Authorization" : "Basic {}".format(base64_message)} 

        post = requests.post(self.SPOTIFY_URL_TOKEN, params=body, headers=headers)
        return self.handleToken(json.loads(post.text))
        
    def handleToken(self, response) -> str:
        auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
        self.REFRESH_TOKEN = response["refresh_token"]
        return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

    def refreshAuth(self) -> str:
        body = {
            "grant_type" : "refresh_token",
            "refresh_token" : self.REFRESH_TOKEN
        }

        post_refresh = requests.post(self.SPOTIFY_URL_TOKEN, data=body, headers=self.HEADER)
        p_back = json.dumps(post_refresh.text)
        
        return self.handleToken(p_back)
