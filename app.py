from flask import Flask, redirect, request, render_template
from handler import Handler

app = Flask(__name__)

#globala variabler
token = ""
genre = ""
        
@app.route('/')
def index():
    '''
    Index-sida med länk för spotify authorization
    '''
    h = Handler()
    authorize = h.getUser()
    return render_template("index.html", authorize=authorize)

@app.route('/callback/')
def callback():
    '''
    Hämtar user-token och skickar tillbaka till applikationen 
    '''
    h = Handler()
    h.getUserToken(request.args['code'])
    global token
    token = h.getAccessToken()
    return redirect("/welcome")

@app.route("/welcome")
def welcome():
    '''
    Välkommnar användaren
    '''
    h = Handler()
    user_data = h.get_current_user(token)
    return render_template("welcome.html", data=user_data, genres="genres")

@app.route("/genres", methods=['POST'])
def genres():
    '''
    Ber användaren välja en genre
    '''
    return render_template("genres.html")

@app.route('/maps', methods=['POST'])
def maps():
    '''
    Ber användaren mata in en tid i min. (Ska implementera google maps API här)
    '''
    data = request.form['switch']
    global genre
    genre = data
    return render_template("maps.html")

@app.route('/success', methods=['POST'])
#Generera spellistan
def success():
    '''
    Genererar en spellista
    '''
    data = request.form['number']
    city = request.form['city']
    h = Handler()
    global genre
    h.genre = genre
    h.song_duration_input = data
    h.city_names = city
    h.convert_min_to_milliseconds()
    h.get_recommendations(token)
    link = h.new_playlist_id
    return render_template("success.html", link=link)

if __name__ == "__main__":
  app.run()