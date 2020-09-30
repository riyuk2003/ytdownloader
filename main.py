from youtube_search import YoutubeSearch
import json
from pytube import YouTube
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from moviepy.editor import *


pathTomp4 = r"yourpathtomp4"
pathTomp3 = r"yourpathtomp3"

#make new app from https://developer.spotify.com/dashboard/ to take the credentials.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("Client ID", "Client Secret"))
username = "username"


def downloadMP4(song, singer):
    searchquery = song + ' ' + singer
    results = json.loads(YoutubeSearch(searchquery, max_results=1).to_json())
    title = results["videos"][0]['title']
    print(title+".mp4")
    if title+".mp4" in os.listdir(pathTomp4):
        print(title, "is already downloaded.")
        return
    link = "https://www.youtube.com"+results["videos"][0]["link"]
    print("Downloading Now:", link)
    x = YouTube(link)
    print(x.streams.get_lowest_resolution().download(pathTomp4))

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

def download(playlistID):
    playlist = sp.playlist(playlistID)

    for i in playlist['tracks']['items']:
        try:
            song = i['track']['name']
            artist = i['track']['artists'][0]['name']
            downloadMP4(song, artist)
        except:
            continue

def convertMP4toMP3():
    mp4list = os.listdir(pathTomp4)
    mp3list = os.listdir(pathTomp3)
    for mp4 in mp4list:
        if mp4 not in mp3list:
            video = VideoFileClip(os.path.join(pathTomp4+'\\'+mp4))
            video.audio.write_audiofile(os.path.join(pathTomp3+'\\'+mp4[:-1]+'3'))



print("Choose:\n1- Download songs of playlist!\n2- convert from mp4 to mp3!\n")
choice = input("Enter your choice: ")
if choice == "1":
    download(input("Please Enter the playlist ID: "))
elif choice == "2":
    convertMP4toMP3()
else:
    print("Invalid choice")
