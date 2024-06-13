import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIPY_CLIENT_ID="70345cca6e654254aae4fc8f10b6f119"
SPOTIPY_CLIENT_SECRET="ceea2c3b96e546ad85925876a72ac9b3"
import json

def spotify_login(cid, secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#change to input statement to get spotify playlist link from user
def get_songs_from_playlist(url):
    sp = spotify_login(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    songListReturn = []
    #url = input("Enter spotify playlist url: ")
    data = sp.playlist_tracks(url, limit=100, offset=0, market=None)
    names = sp.playlist_tracks(url,fields='items.track.name,total', limit=100, offset=0, market=None, additional_types=('track', ))
    artists = sp.playlist_tracks(url,fields='items.track.album.artists.name.name,total', limit=100, offset=0, market=None, additional_types=('track', ))
    length = sp.playlist_tracks(url,fields='items.track.duration_ms',limit=1, offset=0, market=None, additional_types=('track', ))
    popularity = sp.playlist_tracks(url,fields='items.track.popularity',limit=1, offset=0, market=None, additional_types=('track', ))

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

    genrelist = []

    with open('songs.json', 'w') as f:

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

            entry = songName+" by "+ name
            songListReturn.append(entry)

            result = sp.search(entry)
            track = result['tracks']['items'][0]

            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
            for genre in artist["genres"]:
                genrelist.append(genre)

            #top 5 genres
            genrelist = list(dict.fromkeys(genrelist))

            genrelist = genrelist[0:5]
            

            i+=1
        print(songListReturn)
        print(genrelist)
        return songListReturn

#main to test genre implementation
def main():
    get_songs_from_playlist("https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=5e5d6f0b7e4f4f3e")

#call main
main()