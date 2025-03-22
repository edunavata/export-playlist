import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama (cross-platform)
init(autoreset=True)

# Load environment variables from .env
load_dotenv()

# Get credentials from environment
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Verify variables loaded
if not CLIENT_ID or not CLIENT_SECRET:
    print(
        Fore.RED + "[ERROR] Missing SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET in .env"
    )
    exit(1)

# Authentication manager
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# Spotify client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def extract_playlist_id(playlist_url):
    """
    Extract the playlist ID from a Spotify playlist URL.

    :param playlist_url: Full Spotify playlist URL
    :type playlist_url: str
    :return: Playlist ID
    :rtype: str
    """
    pattern = r"playlist\/([a-zA-Z0-9]+)"
    match = re.search(pattern, playlist_url)
    if match:
        return match.group(1)
    else:
        print(Fore.RED + "[ERROR] Invalid playlist URL format.")
        exit(1)


def main():
    print(Fore.CYAN + Style.BRIGHT + "🎵 Spotify Playlist Extractor 🎵\n")

    # Ask user for playlist URL
    playlist_url = input(Fore.YELLOW + "🔗 Enter Spotify playlist URL: ").strip()

    # Extract playlist ID
    playlist_id = extract_playlist_id(playlist_url)

    print(Fore.GREEN + f"\n✅ Extracted Playlist ID: {playlist_id}")

    # Get playlist info
    try:
        playlist = sp.playlist(playlist_id)
    except Exception as e:
        print(Fore.RED + f"\n[ERROR] Failed to fetch playlist: {e}")
        exit(1)

    # Clear the terminal before showing results
    os.system("cls" if os.name == "nt" else "clear")

    # Display playlist name and tracks
    print(Fore.MAGENTA + Style.BRIGHT + f"🎶 Playlist: {playlist['name']}\n")

    tracks = playlist["tracks"]["items"]

    if not tracks:
        print(Fore.RED + "No tracks found in the playlist.")
        exit(0)

    # Show track list
    for idx, item in enumerate(tracks, start=1):
        track = item["track"]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        print(Fore.WHITE + f"{idx}. {track_name} - {artist_name}")


if __name__ == "__main__":
    main()
