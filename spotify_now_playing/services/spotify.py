"""Spotify Web API integration utilities."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

__all__ = ["TrackInfo", "get_current_track"]

load_dotenv()


@dataclass(frozen=True)
class TrackInfo:
    """Represents the playback details for the currently playing track."""

    title: str
    artists: str
    album_art_url: str
    progress_ms: int
    duration_ms: int
    track_id: str
    timestamp: Optional[int]

    @property
    def progress_fraction(self) -> float:
        """Return the playback progress as a floating-point percentage."""

        if not self.duration_ms:
            return 0.0
        return max(0.0, min(self.progress_ms / self.duration_ms, 1.0))


def _get_env(name: str) -> str:
    try:
        value = os.environ[name]
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise RuntimeError(
            f"Environment variable {name!r} is required for Spotify authentication"
        ) from exc
    if not value:
        raise RuntimeError(
            f"Environment variable {name!r} must not be empty for Spotify authentication"
        )
    return value


@lru_cache(maxsize=1)
def _spotify_client() -> spotipy.Spotify:
    """Instantiate the Spotipy client using OAuth credentials."""

    client_id = _get_env("SPOTIPY_CLIENT_ID")
    client_secret = _get_env("SPOTIPY_CLIENT_SECRET")
    redirect_uri = _get_env("SPOTIPY_REDIRECT_URI")

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-playback-state,user-read-currently-playing",
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def get_current_track() -> Optional[TrackInfo]:
    """Retrieve metadata about the track currently being played by the user."""

    client = _spotify_client()
    current_track = client.current_playback()
    item = current_track.get("item") if current_track else None
    if not item:
        return None

    images = item.get("album", {}).get("images") or []
    first_image = images[0] if images else {}

    return TrackInfo(
        title=item.get("name", ""),
        artists=", ".join(artist.get("name", "") for artist in item.get("artists", [])),
        album_art_url=first_image.get("url", ""),
        progress_ms=current_track.get("progress_ms") or 0,
        duration_ms=item.get("duration_ms") or 0,
        track_id=item.get("id", ""),
        timestamp=current_track.get("timestamp"),
    )
