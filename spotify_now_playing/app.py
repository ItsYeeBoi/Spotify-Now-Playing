"""Main application module for the Spotify Now Playing GUI."""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

import customtkinter as ctk
from requests import RequestException

from .services import TrackInfo, get_current_track
from .ui import SongDisplayWidgets, build_ui

__all__ = ["SpotifyNowPlayingApp", "run_app"]

logger = logging.getLogger(__name__)

TrackSupplier = Callable[[], Optional[TrackInfo]]


@dataclass
class PlaybackState:
    """Internal state tracking for the polling loop."""

    track_id: Optional[str] = None
    last_timestamp: int = 0


class SpotifyNowPlayingApp:
    """Tkinter application that displays the user's currently playing track."""

    def __init__(
        self,
        *,
        poll_interval: float = 0.1,
        track_supplier: TrackSupplier = get_current_track,
        root: Optional[ctk.CTk] = None,
    ) -> None:
        self._poll_interval = poll_interval
        self._track_supplier = track_supplier

        if root is None:
            ctk.set_appearance_mode("dark")
            self.root = ctk.CTk()
        else:
            self.root = root
        self.root.title("Spotify Now Playing")

        self.widgets: SongDisplayWidgets = build_ui(self.root)
        self._state = PlaybackState()
        self._polling_thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Start the polling thread and enter the Tk main loop."""

        self._start_polling()
        self.root.mainloop()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _start_polling(self) -> None:
        if self._polling_thread and self._polling_thread.is_alive():
            return

        self._polling_thread = threading.Thread(
            target=self._poll_loop,
            daemon=True,
            name="SpotifyPollingThread",
        )
        self._polling_thread.start()

    def _poll_loop(self) -> None:
        while self.root.winfo_exists():
            track = self._safe_fetch_track()
            self.root.after(0, lambda t=track: self._apply_track_update(t))
            time.sleep(self._poll_interval)

    def _safe_fetch_track(self) -> Optional[TrackInfo]:
        try:
            return self._track_supplier()
        except Exception as exc:  # pragma: no cover - defensive guard
            logger.exception("Failed to fetch track information: %s", exc)
            return None

    def _apply_track_update(self, track: Optional[TrackInfo]) -> None:
        if track is None:
            self._render_idle_state()
            return

        if track.timestamp is not None and track.timestamp < self._state.last_timestamp:
            return

        if track.timestamp is not None:
            self._state.last_timestamp = track.timestamp

        if track.track_id != self._state.track_id:
            self._state.track_id = track.track_id
            self.widgets.song_label.clear()
            self.widgets.artist_label.clear()

        self.widgets.song_label.set_text(track.title)
        self.widgets.artist_label.set_text(track.artists)

        if track.album_art_url:
            try:
                self.widgets.album_label.set_image(track.album_art_url)
            except RequestException as exc:  # pragma: no cover - network failure
                logger.warning("Unable to load album artwork: %s", exc)
        else:
            self.widgets.album_label.clear()

        self.widgets.progress_bar.set(track.progress_fraction)
        self.widgets.current_time_label.configure(
            text=self._format_time(track.progress_ms)
        )
        self.widgets.total_time_label.configure(
            text=self._format_time(track.duration_ms)
        )

    def _render_idle_state(self) -> None:
        self._state = PlaybackState()
        self.widgets.song_label.set_text("No track playing")
        self.widgets.artist_label.clear()
        self.widgets.album_label.clear()
        self.widgets.progress_bar.set(0)
        self.widgets.current_time_label.configure(text="0:00")
        self.widgets.total_time_label.configure(text="0:00")

    @staticmethod
    def _format_time(milliseconds: int) -> str:
        minutes, seconds = divmod(max(milliseconds, 0) // 1000, 60)
        return f"{minutes}:{seconds:02}"


def run_app() -> None:
    """Convenience wrapper used by the console entry point."""

    app = SpotifyNowPlayingApp()
    app.run()
