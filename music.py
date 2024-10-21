import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os




spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET))

#change to input statement to get spotify playlist link from user
url = "https://open.spotify.com/playlist/63srYXKnWf2b6SP3Rf7Hau?si=d4481a15907d41c0"
def get_songs_from_playlist(url):
    SPOTIPY_CLIENT_ID=os.getenv("HUGGINGFACE_API_KEY")
    SPOTIPY_CLIENT_SECRET=os.getenv("HUGGINGFACE_API_KEY")
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET))
    songListReturn = []
    #url = input("Enter spotify playlist url: ")
    data = spotify.playlist_tracks(url, limit=100, offset=0, market=None)
    names = spotify.playlist_tracks(url,fields='items.track.name,total', limit=100, offset=0, market=None, additional_types=('track', ))
    artists = spotify.playlist_tracks(url,fields='items.track.album.artists.name.name,total', limit=100, offset=0, market=None, additional_types=('track', ))
    length = spotify.playlist_tracks(url,fields='items.track.duration_ms',limit=1, offset=0, market=None, additional_types=('track', ))
    popularity = spotify.playlist_tracks(url,fields='items.track.popularity',limit=1, offset=0, market=None, additional_types=('track', ))

    trackCount = 0
    trackCount = trackCount + len(artists['items'])

    i=0

    song_list = list(names.values())
    artist_list = list(artists.values())
    length_list = list(length.values())
    pop_length = list(popularity.values())
    artistList = artist_list[0]
    songList = song_list[0]
    lengthList = length_list[0]
    popList = pop_length[0]

    for song in songList:
        name = songList[i]
        songName=list(name.values())
        songName=str(songName)
        songName=songName.replace("[{'name': '","")
        songName = songName.replace("'}]","")
        if (songName[0:2]=="[{"):
            songName=songName.replace('''[{'name': "''',"")
            songName = songName.replace('''"}]''',"")

        notrack = list(artistList[i].values()) #no track

        noalbum = notrack[0] #no album
        noalbum = list(noalbum.values())

        noartists = noalbum[0] #no album
        noartists = list(noartists.values())

        nourl = noartists[0] #no album
        nourl = nourl[0]
        name = nourl['name']
        songListReturn.append(songName+" by "+ name)

        i+=1
    print(songListReturn)
    return songListReturn
