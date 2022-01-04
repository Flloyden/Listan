# Listan

Listan är en webbapplikationsom genererar en spellista baserat på en viss tid och färdmedel med hälp av Google maps API. Spellistan baseras också på en specifik genre som man väljer tack vare Spotify API. Listan hjälper dig på din kommande resa!

## Installation

OBS: För att kunna köra applikationen måste du lägga till google maps API-nyckel samt Spotify klient-id och klienthemlighet

Denna applikationen kräver det att man har python installerat. Kontrollera detta genom: **python --version** eller **python3 --version**

1. Ladda ner Listan från github och öppna mappen i en terminal, som t.ex. Windows PowerShell. 
2. Skapa en virtuell miljö genom: python -m venv venv
3. Aktivera sedan miljön med: venv\Scripts\activate
4. Kör kommandot: pip install -r requirements.txt
5. Efter allt är installerat kan du starta applikationen med: flask run
6. Nu kan du öppna applikationen i din webbläsare på: http://127.0.0.1:5000/

För att avsluta applikationen kör Ctrl+C i terminalen

## Installation MacOS

OBS: För att kunna köra applikationen måste du lägga till google maps API-nyckel samt Spotify klient-id och klienthemlighet

Denna applikationen kräver det att man har python installerat. Kontrollera detta genom: **python --version** eller **python3 --version**

1. Ladda ner Listan från github och öppna mappen i en terminal. 
2. Skapa en virtuell miljö genom: virtualenv venv
3. Aktivera sedan miljön med: source venv/bin/activate
4. Kör kommandot: pip install -r requirements.txt
5. Efter allt är installerat kan du starta applikationen med: flask run
6. Nu kan du öppna applikationen i din webbläsare på: http://127.0.0.1:5000/

För att avsluta applikationen kör Ctrl+C i terminalen

### Lägg till klient-ID och klienthemlighet

handler.py är den fil som behöver modifieras. Inom handler.py måste du ange ditt klient-ID och klienthemlighet

### Lägg till Google maps API

maps.html är den fil som behöver modifieras. Inom maps.html måste du ange din API nyckel på rad 59

### ERROR: scripts is disabled on this system

Som administratör kan du ställa in körningspolicyn genom att skriva detta i ditt PowerShell-fönster: **Set-ExecutionPolicy RemoteSigned** 

När du är klar kan du ställa tillbaka policyn till dess standardvärde med: **Set-ExecutionPolicy Restricted**
