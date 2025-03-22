import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get credentials from environment
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

print(CLIENT_ID, CLIENT_SECRET)

# Verify variables loaded
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Environment variables not set. Check your .env file.")

# Authentication manager
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# Spotify client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Example: get playlist data
playlist_id = "5JUAGSYzfOef8m1yq6ObSY"
playlist = sp.playlist(playlist_id)

# Print playlist name and tracks
print(f"Playlist: {playlist['name']}")
for item in playlist["tracks"]["items"]:
    track = item["track"]
    print(f"{track['name']} - {track['artists'][0]['name']}")
