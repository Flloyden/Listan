from flask_spotify_auth import SpotifyOauth
import json
import requests
import math

class Handler:
    def __init__(self) -> None:
        self.SpotifyOauth = SpotifyOauth()
        self.CLIENT_ID = "YOUR_CLIENT_ID"
        self.CLIENT_SECRET = "YOUR_CLIENT_SECRET"
        self.CALLBACK_URL = "http://127.0.0.1"
        self.PORT = "5000"
        self.SCOPE = "user-read-private user-read-email user-library-modify playlist-modify-private playlist-read-collaborative playlist-modify-public user-library-read playlist-read-private"
        self.TOKEN_DATA = ""
        self.spotify_token = ""
        self.tracks = ""
        self.new_playlist_id = ""
        self.current_user = ""
        self.genres = []
        self.song_duration = []
        self.song_duration_input = 0
        self.genre = ""
        self.average_song_length = 197000 #millisekunder
        self.song_limit = ""
        self.city_names = ""
    
    def getUser(self):
        return self.SpotifyOauth.getAuth(self.CLIENT_ID, "{}:{}/callback/".format(self.CALLBACK_URL, self.PORT), self.SCOPE)

    def getUserToken(self, code):
        self.TOKEN_DATA = self.SpotifyOauth.getToken(code, self.CLIENT_ID, self.CLIENT_SECRET, "{}:{}/callback/".format(self.CALLBACK_URL, self.PORT))
    
    def refreshToken(self, time):
        time.sleep(time)
        self.TOKEN_DATA = self.SpotifyOauth.refreshAuth()

    def getAccessToken(self):
        return self.TOKEN_DATA

    def convert_min_to_milliseconds(self):
        milliseconds = int(self.song_duration_input) * 1000
        amount_of_songs = milliseconds / self.average_song_length
        songs_required = math.trunc(amount_of_songs)
        self.song_limit = songs_required
        return milliseconds

    def get_recommendations(self, token):
        print("Finding recommendations...")
        endpoint = "https://api.spotify.com/v1/recommendations?"
        limit = str(self.song_limit)
        seed_artist = ""
        seed_genres = self.genre
        market = "SE"
        seed_tracks = ""
        query = f"{endpoint}limit={limit}&market={market}&seed_genres={seed_genres}&seed_artists={seed_artist}&seed_tracks={seed_tracks}"
        response = requests.get(query, headers={"Content-type": "application/json", 
            "Authorization": "Bearer {}".format(token)})
        response_json = response.json()

        for item in response_json["tracks"]:
            id = item["id"]
            self.tracks += ("spotify:track:" + id + ",")
            duration = item["duration_ms"]
            self.song_duration.append(duration)

        self.tracks = self.tracks[:-1]

        self.add_to_playlist(token)

    def get_current_user(self, token):
        print("Finding current user...")
        query = "https://api.spotify.com/v1/me"
        response = requests.get(query, headers={"Content-type": "application/json", 
            "Authorization": "Bearer {}".format(token)})
        response_json = response.json()
        user_display_name = response_json["display_name"]
        user_id = response_json["id"]
        return user_display_name, user_id
    
    #Används inte?
    def get_genre(self):
        print("Finding genres...")
        query = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        response = requests.get(query, headers={"Content-type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        for i in response_json["genres"]:
            self.genres.append(i)

        return self.genres
    
    def create_playlist(self, token):
        print("Trying to create playlist")
        query = "https://api.spotify.com/v1/users/1158761339/playlists"
        test = self.city_names
        res = test.split()
        from_place = str(res[0])[:-1]
        to_place = str(res[2])[:-1]
        playlist_name = "Listan - " + from_place + " till " + to_place
        playlist_description = "Denna spellistan har genererats med hjälp av Listan. En spellista som tar dig från " + from_place + " till " + to_place + " med musik i din smak."

        request_body = json.dumps({
            "name": playlist_name,
            "description": playlist_description,
            "public": False
        })

        response = requests.post(query, data=request_body, headers={
            "Content-type": "application/json", 
            "Authorization": "Bearer {}".format(token)
        })

        response_json = response.json()
        
        return response_json["id"]

    def add_to_playlist(self, token):
        self.new_playlist_id = self.create_playlist(token)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        print("Trying to add songs to playlist")

        response = requests.post(query, headers={
            "Content-type": "application/json", 
            "Authorization": "Bearer {}".format(token)
        })

        print(response.json)