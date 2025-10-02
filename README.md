# Spotify Now Playing

A polished CustomTkinter desktop client that surfaces the track currently playing on your Spotify account. The application shows the title, artists, album artwork, and playback progress using a minimal, dark themed interface.

## Features

- **Real-time Spotify integration** powered by the official Web API.
- **Modern interface** implemented with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) widgets.
- **Smooth marquee labels** that automatically scroll long song titles or artist lists.
- **Album artwork rendering** with rounded corners for a consistent look.
- **Responsive progress indicator** displaying both elapsed and total track time.

The `spotify_now_playing` package exposes reusable service and UI layers, while `main.py` remains as a backwards-compatible launcher.

## Getting started

### Prerequisites

- Python 3.8 or later
- A Spotify Developer application with a client ID and client secret
- An active Spotify account

### Installation

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/your-username/spotify-now-playing.git
   cd spotify-now-playing
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Provide your Spotify credentials. Create a `.env` file in the project root with the following values:
   ```env
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=your_registered_redirect_uri
   ```

### Running the application

After completing the setup steps above, you can start the desktop client using either of the following commands:

```bash
python -m spotify_now_playing
# or
python main.py
```

On first launch a browser window will prompt you to authorize the application against your Spotify account. Once authorized, the window will continuously display the track currently playing on your account.

## Environment variables

The application expects the following environment variables (set via `.env` or your shell):

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`

Missing or empty values will raise an informative error during start-up.

## License

This project is provided as-is without any specific license. Adapt it to suit your needs.