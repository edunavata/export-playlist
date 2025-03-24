# 🎵 Spotify Playlist Extractor

Extract and list songs from any Spotify playlist (public, private, or collaborative) using Python and Spotify OAuth.

## Features

- Supports public, private, and collaborative playlists.
- Simple and clean CLI interface.
- Exports playlists to JSON in a simplified format.

## Requirements

- Python 3.8+
- Spotify Developer Account (to get API credentials)

## Setup

1. Clone the repository and install dependencies:

    ```bash
    git clone https://github.com/edunavata/export-playlist.git
    cd export-playlist
    ```

2. (Optional) Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a Spotify App on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

5. Set the Redirect URI in your Spotify App:

    ```
    http://localhost:8888/callback
    ```

6. Create a `.env` file in the project root with your credentials:

    ```
    SPOTIPY_CLIENT_ID=your_client_id
    SPOTIPY_CLIENT_SECRET=your_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
    ```

    Or copy the provided `.env.demo` and fill in your values.

## Usage

Display playlist tracks in the terminal:

```bash
python main.py
```

Export the playlist to JSON:

```bash
python main.py --export
```

Specify an output file name:

```bash
python main.py --export --output my_playlist.json
```

## JSON Export Format

The exported JSON file contains the playlist name and a list of songs with their names and main artist:

```json
{
  "playlist": "Playlist Name",
  "songs": [
    {
      "name": "Track Name",
      "artist": "Artist Name"
    }
  ]
}
```

## Project Structure

- `main.py`: Main script
- `.env.demo`: Example environment variables file
- `requirements.txt`: Project dependencies
