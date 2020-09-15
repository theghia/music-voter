import os
import sys
import json
import spotipy as sp
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
# username = input("What is your Spotify username? ")
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

token = None

spotifyObject = sp.Spotify(auth_manager=
SpotifyOAuth(
    scope=scope,
    client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
    client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI')))

devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']

# Get track information
track = spotifyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

if artist != "":
    print(f"Currently playing {artist} - {track}")

# User information
user = spotifyObject.current_user()
displayName = user['display_name']
follower = user['followers']['total']

while True:
    print()
    print(f">>> Welcome to Spotify {displayName}:")
    print(f">>> You have {follower} followers")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Enter your choice: ")

    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name? ")
        print()

        # Get search results
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")

        # Print artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(f"{artist['followers']['total']} followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract data from album
        albumResults = spotifyObject.artist_albums(artistID)
        print(json.dumps(albumResults))
        print(albumResults['items'])
        albumResults = albumResults['items']

        for album in albumResults:
            print(f"ALBUM: {album['name']}")
            albumID = album['id']
            albumArt = album['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for track in trackResults:
                print(f"{z}: {track['name']}")
                trackURIs.append(track['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        # See album art
        while True:
            songSelection = input("Enter a song number to see the album art: ")
            if songSelection == "x":
                break
            trackSelectionList = [trackURIs[int(songSelection)]]
            spotifyObject.start_playback(deviceID, None, trackSelectionList)
            webbrowser.open(trackArt[int(songSelection)])
    elif choice == "1":
        break
