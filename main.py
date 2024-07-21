from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = ----
CLIENT_SECRET = ----
REDIRECT_URL = ---

# Get titles of song using BeautifulSoup
endpoint_start = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

contents = requests.get(f"{endpoint_start}{date}").text
soup = BeautifulSoup(contents, "html.parser")

get_titles = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
get_artists = soup.find_all("span", class_="chart-element__information__artist text--truncate color--secondary")

hundred_titles = [title.getText() for title in get_titles]
artists = [artist.getText() for artist in get_artists]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
for index in range(len(hundred_titles)):
    result = sp.search(q=f'artist:{artists[index]} track:{hundred_titles[index]}', type='track', limit=1, market='US')
    try:
        song_uris.append(result['tracks']['items'][0]['uri'])
    except:
        print(f'{hundred_titles[index]} not found.')

print(song_uris)
new_playlist = sp.user_playlist_create(user=user_id, name=f"{date} : Billboard 100", description=f"Most popular songs of {date}", public=False)
print(new_playlist)
playlist_id = "46I7hbLh8rxbLiB98QGT0O"

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)