import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Initialize Spotipy client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-read-playback-state,user-read-currently-playing",
    )
)


def get_current_song():
    current_track = sp.current_playback()
    if current_track and current_track["item"]:
        song_name = current_track["item"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in current_track["item"]["artists"]]
        )
        album_art_url = current_track["item"]["album"]["images"][0]["url"]
        progress_ms = current_track["progress_ms"]
        duration_ms = current_track["item"]["duration_ms"]
        track_id = current_track["item"]["id"]

        return song_name, artists, album_art_url, progress_ms, duration_ms, track_id
    else:
        return None, None, None, None, None, None
