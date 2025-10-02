"""Service layer abstractions for interacting with external APIs."""

from .spotify import TrackInfo, get_current_track

__all__ = ["TrackInfo", "get_current_track"]
