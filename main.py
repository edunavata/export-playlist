import os
import re
import json
import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama (cross-platform)
init(autoreset=True)

# Load environment variables from .env
load_dotenv()

# Get credentials from environment
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Verify variables loaded
if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    print(
        Fore.RED
        + "[ERROR] Missing SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET or SPOTIPY_REDIRECT_URI in .env"
    )
    exit(1)

# Spotify OAuth authentication (Authorization Code Flow)
scope = "playlist-read-private playlist-read-collaborative"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    show_dialog=False,  # Pon True si quieres forzar login en cada ejecución
)

# Spotify client con el token de usuario
sp = spotipy.Spotify(auth_manager=sp_oauth)


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


def fetch_playlist(playlist_id):
    """
    Fetch the playlist data from Spotify.

    :param playlist_id: Spotify playlist ID
    :type playlist_id: str
    :return: Playlist data
    :rtype: dict
    """
    try:
        playlist = sp.playlist(playlist_id)
        return playlist
    except Exception as e:
        print(Fore.RED + f"\n[ERROR] Failed to fetch playlist: {e}")
        exit(1)


def display_tracks(playlist):
    """
    Display tracks from the playlist in the terminal.

    :param playlist: Playlist data
    :type playlist: dict
    """
    os.system("cls" if os.name == "nt" else "clear")

    print(Fore.MAGENTA + Style.BRIGHT + f"🎶 Playlist: {playlist['name']}\n")

    tracks = playlist["tracks"]["items"]

    if not tracks:
        print(Fore.RED + "No tracks found in the playlist.")
        return

    for idx, item in enumerate(tracks, start=1):
        track = item["track"]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        print(Fore.WHITE + f"{idx}. {track_name} - {artist_name}")


def export_to_json(playlist, output_file="playlist.json"):
    """
    Export the playlist data to a simplified JSON file.

    :param playlist: Playlist data
    :type playlist: dict
    :param output_file: Output file name
    :type output_file: str
    """
    try:
        simplified_playlist = {"playlist": playlist["name"], "songs": []}

        # Manejar paginación para obtener todas las canciones
        tracks = playlist["tracks"]
        while tracks:
            for item in tracks["items"]:
                track = item["track"]
                song = {"name": track["name"], "artist": track["artists"][0]["name"]}
                simplified_playlist["songs"].append(song)

            # Si hay más páginas, las recorremos
            if tracks["next"]:
                tracks = sp.next(tracks)
            else:
                break

        # Guardar el JSON simplificado
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(simplified_playlist, f, ensure_ascii=False, indent=4)

        print(Fore.GREEN + f"\n✅ Playlist exported successfully to {output_file}")

    except Exception as e:
        print(Fore.RED + f"\n[ERROR] Failed to export playlist: {e}")


def parse_arguments():
    """
    Parse command-line arguments.

    :return: Parsed arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="🎵 Spotify Playlist Extractor - Extract and export Spotify playlists"
    )
    parser.add_argument(
        "-e", "--export", action="store_true", help="Export the playlist to JSON"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="playlist.json",
        help="Output JSON file name (default: playlist.json)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    print(Fore.CYAN + Style.BRIGHT + "🎵 Spotify Playlist Extractor 🎵\n")

    # Ask user for playlist URL
    playlist_url = input(Fore.YELLOW + "🔗 Enter Spotify playlist URL: ").strip()

    # Extract playlist ID
    playlist_id = extract_playlist_id(playlist_url)
    print(Fore.GREEN + f"\n✅ Extracted Playlist ID: {playlist_id}")

    # Get playlist info
    playlist = fetch_playlist(playlist_id)

    if args.export:
        export_to_json(playlist, args.output)
    else:
        display_tracks(playlist)


if __name__ == "__main__":
    main()
