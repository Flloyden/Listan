# Listan

Listan är en webbapplikationsom genererar en spellista baserat på en viss tid och färdmedel med hälp av Google maps API. Spellistan baseras också på en specifik genre som man väljer tack vare Spotify API. Listan hjälper dig på din kommande resa!

## Installation

OBS: För att kunna köra applikationen måste du lägga till din google maps API samt Spotify klient-id och klienthemlighet

Denna applikationen kräver det att man har python installerat. Kontrollera detta genom: **python --version** eller **python3 --version**

1. Fixa en spotify applikation (instruktioner längre ner)
2. Ladda ner Listan från github och öppna mappen i en terminal, som t.ex. Windows PowerShell. 
3. Skapa en virtuell miljö genom: python -m venv venv
4. Aktivera sedan miljön med: venv\Scripts\activate
5. Kör kommandot: pip install -r requirements.txt
6. Efter allt är installerat kan du starta applikationen med: flask run
7. Nu kan du öppna applikationen i din webbläsare på: http://127.0.0.1:5000/

För att avsluta applikationen kör Ctrl+C i terminalen

## Installation MacOS

OBS: För att kunna köra applikationen måste du lägga till din google maps API samt Spotify klient-id och klienthemlighet

Denna applikationen kräver det att man har python installerat. Kontrollera detta genom: **python --version** eller **python3 --version**

1. Fixa en spotify applikation (instruktioner längre ner)
2. Ladda ner Listan från github och öppna mappen i en terminal. 
3. Skapa en virtuell miljö genom: virtualenv venv
4. Aktivera sedan miljön med: source venv/bin/activate
5. Kör kommandot: pip install -r requirements.txt
6. Efter allt är installerat kan du starta applikationen med: flask run
7. Nu kan du öppna applikationen i din webbläsare på: http://127.0.0.1:5000/

För att avsluta applikationen kör Ctrl+C i terminalen

### Spotify applikation
För att denna applikation ska kunna fungera så måste du skapa en applikation på spotify.

1. Gå till https://developer.spotify.com/dashboard/ och logga in
2. Tryck på **CREATE AN APP** och fyll i nödvändig information
3. Tryck sedan på **edit settings** lägg till **http://127.0.0.1:5000/callback/** som Redirect URI och spara
4. Spara **Client ID** och **Client Secret** för att sedan klistra in dem i handler.py

### Callback URL
Callback och porten listas som standard som http://127.0.0.1 och 5000. Om Callback-url lämnas som standard, måste http://127.0.0.1:5000/callback/ registreras som en omdirigerings-uri i Spotify Developer Dashboard.

### Lägg till klient-ID och klienthemlighet

handler.py är den fil som behöver modifieras. Inom handler.py måste du ange ditt klient-ID och klienthemlighet

### Lägg till Google maps API

maps.html är den fil som behöver modifieras. Inom maps.html måste du ange din API nyckel på rad 59

### ERROR: scripts is disabled on this system

Som administratör kan du ställa in körningspolicyn genom att skriva detta i ditt PowerShell-fönster: **Set-ExecutionPolicy RemoteSigned** 

När du är klar kan du ställa tillbaka policyn till dess standardvärde med: **Set-ExecutionPolicy Restricted**
