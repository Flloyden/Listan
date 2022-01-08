from auth import Auth
import json
import requests
import math

class Handler:
    def __init__(self) -> None:
        self.Auth = Auth()
        self.client_id = "YOUR_CLIENT_ID"
        self.client_secret = "YOUR_CLIENT_SECRET"
        self.callback_url = "http://127.0.0.1"
        self.port = "5000"
        self.scope = "user-read-private user-read-email user-library-modify playlist-modify-private playlist-read-collaborative playlist-modify-public user-library-read playlist-read-private"
        self.token_data = ""
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
        self.user_id = ""
    
    def getUser(self) -> str:
        '''
        Returnerar infromation om token, callback url och scope
        '''
        return self.Auth.getAuth(self.client_id, "{}:{}/callback/".format(self.callback_url, self.port), self.scope)

    def getUserToken(self, code) -> None:
        '''
        Lägger till infromation om token
        '''
        self.token_data = self.Auth.getToken(code, self.client_id, self.client_secret, "{}:{}/callback/".format(self.callback_url, self.port))
    
    def refreshToken(self, time) -> None:
        time.sleep(time)
        self.token_data = self.Auth.refreshAuth()

    def getAccessToken(self) -> str:
        '''
        Retuenerar data om spotify token
        '''
        return self.token_data

    def convert_min_to_milliseconds(self) -> None:
        '''
        Gör om sekunder till millisekunder och lägger till hur många antal låtar som behövs
        '''
        milliseconds = int(self.song_duration_input) * 1000
        amount_of_songs = milliseconds / self.average_song_length
        songs_required = math.trunc(amount_of_songs)
        self.song_limit = songs_required

    def get_recommendations(self, token) -> None:
        '''
        Hämtar antal låtar baserat på genre som användaren valt och lägger till dem i en sträng
        '''
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

    def get_current_user(self, token) -> str:
        '''
        Hämtar information om användarenoch returnerar användarnamnet samt user_id
        '''
        print("Finding current user...")
        query = "https://api.spotify.com/v1/me"
        response = requests.get(query, headers={"Content-type": "application/json", 
            "Authorization": "Bearer {}".format(token)})
        response_json = response.json()
        user_display_name = response_json["display_name"]
        user_id = response_json["id"]
        self.user_id = user_id
        return user_display_name, user_id
    
    #Används inte?
    def get_genre(self) -> list:
        '''
        Hämtar available-genre-seeds från spotify, lägger dem i en lista och returnerar listan 
        '''
        print("Finding genres...")
        query = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        response = requests.get(query, headers={"Content-type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        for i in response_json["genres"]:
            self.genres.append(i)

        return self.genres
    
    def create_playlist(self, token) -> str:
        '''
        Skapar en spellista och returnerar dess id
        '''
        print("Trying to create playlist")
        self.get_current_user(token)
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
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

    def add_to_playlist(self, token) -> None:
        '''
        Lägger till låtar i den nyss gjorda spellistan
        '''
        self.new_playlist_id = self.create_playlist(token)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        print("Trying to add songs to playlist")

        response = requests.post(query, headers={
            "Content-type": "application/json", 
            "Authorization": "Bearer {}".format(token)
        })

        print(response.json)