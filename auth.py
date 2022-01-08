import base64
import json
import requests

class Auth:

    def __init__(self) -> None:
        self.spotify_url_token = 'https://accounts.spotify.com/api/token/'
        self.header = 'application/x-www-form-urlencoded'
        self.refresh_token = ''
        
    def getAuth(self, client_id, redirect_uri, scope) -> str:
        '''
        Returnerar en sträng med data för authorization
        '''
        spotify_url_auth = 'https://accounts.spotify.com/authorize/?'
        data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(spotify_url_auth, client_id, redirect_uri, scope) 
        return data

    def getToken(self, code, client_id, client_secret, redirect_uri) -> str:
        '''
        Skickar data till Spotify och hämtar token
        '''
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
        headers = {"Content-Type" : self.header, "Authorization" : "Basic {}".format(base64_message)} 

        post = requests.post(self.spotify_url_token, params=body, headers=headers)
        return self.handleToken(json.loads(post.text))
        
    def handleToken(self, response) -> str:
        '''
        Hanterar datan som returneras från Spotify
        '''
        auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
        self.refresh_token = response["refresh_token"]
        return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

    def refreshAuth(self) -> str:
        '''
        Uppdaterar token
        '''
        body = {
            "grant_type" : "refresh_token",
            "refresh_token" : self.refresh_token
        }

        post_refresh = requests.post(self.spotify_url_token, data=body, headers=self.header)
        p_back = json.dumps(post_refresh.text)
        
        return self.handleToken(p_back)
