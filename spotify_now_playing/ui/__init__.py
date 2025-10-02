"""UI components for the Spotify Now Playing application."""

from .elements import SongDisplayWidgets, build_ui
from .widgets import AlbumLabel, SmoothScrollingLabel

__all__ = [
    "AlbumLabel",
    "SmoothScrollingLabel",
    "SongDisplayWidgets",
    "build_ui",
]
