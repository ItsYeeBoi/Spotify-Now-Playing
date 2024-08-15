# Spotify Now Playing

**Spotify Now Playing** is a Python-based desktop application that displays the currently playing song on Spotify, including the album artwork, song title, artist(s), and a progress bar indicating the current position in the track. The application is built using `CustomTkinter` for a modern and customizable user interface.

## Features

- **Real-time Spotify Integration**: Fetches and displays the currently playing song from your Spotify account.
- **Customizable UI**: Built with `CustomTkinter`, offering a dark mode with smooth scrolling text for long song titles and artist names.
- **Album Art Display**: Shows the album artwork of the currently playing track.
- **Progress Bar**: Displays the progress of the current track with start and end times.
- **Scrolling Text**: Automatically scrolls text for long song titles and artist names, with a smooth forward and backward scrolling effect.
- **Responsive Layout**: Adapts the display to different screen sizes while maintaining a consistent look and feel.

## Installation

### Prerequisites

- Python 3.7 or later
- Spotify Developer Account with Client ID and Client Secret
- A valid Spotify account

### Setting Up the Environment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/spotify-now-playing.git
   cd spotify-now-playing
2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
4. **Set Up Spotify Credentials**:
- Create a `.env` file in the project root directory.
- Add your Spotify credentials to the .env file:
makefile

    ```
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=your_redirect_uri
