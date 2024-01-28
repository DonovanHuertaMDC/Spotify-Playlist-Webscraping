from bs4 import BeautifulSoup
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

client_ID = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_URI = os.getenv("SPOTIPY_REDIRECT_URI")
scope = "playlist-modify-private"
user_name = os.getenv("SPOTIPY_USER_NAME")
song_titles = []
uri_songs = []
singers = []
hits = {}
x = 1
y = 0
TOP_N = 1


#Functions.
def singers_list():
    global x, singers
    for m in range(len(singers_and_songs)):
        each_singer = singers_and_songs[x]
        singers.append(each_singer)
        x += 2
        if x > len(singers_and_songs):
            break

def songs_list():
    global y
    global song_titles
    for name_of_song in range(len(singers_and_songs)):
        songs = singers_and_songs[y]
        song_titles.append(songs)
        y += 2
        if y >= len(singers_and_songs):
            break

def songs_dict():
    global TOP_N, song_titles, singers
    for h in range(0, 100):
        hits[f"TOP {TOP_N}"] = {"Song": ""}
        hits[f"TOP {TOP_N}"] = {"Artist": ""}
        hits[f"TOP {TOP_N}"]["Song"] = song_titles[h]
        hits[f"TOP {TOP_N}"]["Artist"] = singers[h]
        TOP_N += 1

def dict_singers_and_songs():
    global singers, song_titles
    for p in range(len(song_titles)):
        print(f"{singers[p]} - {song_titles[p]}")


# SPOTIFY AUTHENTICATION.
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_ID,
        client_secret=client_secret,
        redirect_uri=redirect_URI,
        scope=scope,
        username = user_name,
        cache_path ="token.txt",
        open_browser=False,))


user_id = sp.current_user()["id"]

#Billboard Hot 100™ – Billboard
desired_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
url_top_songs = f"https://www.billboard.com/charts/hot-100/{desired_date}"
year = desired_date.split("-")[0]


response = requests.get(url_top_songs)
billboard_top_music = response.text
soup = BeautifulSoup(billboard_top_music, "html.parser") #En forma de lista

title_list = soup.title.get_text()
searching_name = soup.find_all(class_=re.compile("a-no-trucate"))#Search some words you want to search in class

#Songs and singer's interleaved list
singers_and_songs = [song.get_text().strip() for song in searching_name]

singers_list()
songs_list()
songs_dict()

print(title_list)
print(hits)
print(song_titles)
print(singers)


#Create a list of URI songs.
for n in range(len(song_titles)):
    result = sp.search(q=f"artist:{singers[n]} track:{song_titles[n]} year:{year}", type="track", limit=1)
    try:
        soundtrack = result["tracks"]["items"][0]["uri"]
        #print(soundtrack)
        uri_songs.append(soundtrack)
    except IndexError as ie:
        print(f"Sorry: {singers[n]} - {song_titles[n]} doesn\'t found.")

print(uri_songs)


#Create a playlist with the input date.
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{desired_date} Billboard 100",
                                   public=False,
                                   description="This playlist was created according to the top 100 music in some specific date")
print(playlist)


#Add tracks into the playlist.
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=uri_songs)
print("\nThe songs were added into the playlist.")




