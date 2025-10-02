import threading
import time

import customtkinter as ctk

from gui_elements import create_gui_elements
from spotify_api import get_current_song

# Global variables to track the current song and artist
current_song_name = None
current_artist_name = None
current_track_id = None
last_playback_timestamp = 0


def update_song_details(root, elements):
    global current_song_name, current_artist_name, current_track_id, last_playback_timestamp
    (
        song_label,
        artist_label,
        album_label,
        progress_bar,
        current_time_label,
        total_time_label,
    ) = elements

    (
        song_name,
        artists,
        album_art_url,
        progress_ms,
        duration_ms,
        track_id,
        playback_timestamp,
    ) = get_current_song()

    if song_name:
        if (
            playback_timestamp is not None
            and playback_timestamp < last_playback_timestamp
        ):
            root.after(100, update_song_details, root, elements)
            return

        if playback_timestamp is not None:
            last_playback_timestamp = playback_timestamp

        if track_id != current_track_id:
            current_track_id = track_id
            if hasattr(song_label, "scroll_after_id"):
                song_label.after_cancel(song_label.scroll_after_id)
            if hasattr(artist_label, "scroll_after_id"):
                artist_label.after_cancel(artist_label.scroll_after_id)

        if song_name != current_song_name:
            current_song_name = song_name
            song_label.set_text(song_name)

        if artists != current_artist_name:
            current_artist_name = artists
            artist_label.set_text(artists)

        if album_art_url:
            album_label.set_image(album_art_url)

        progress_value = progress_ms
        total_duration = duration_ms

        if total_duration and progress_value is not None:
            progress_bar.set(progress_value / total_duration)

        progress_ms = progress_value or 0
        duration_ms = total_duration or 0

        current_time_label.configure(
            text=f"{progress_ms // 60000}:{(progress_ms // 1000) % 60:02}"
        )
        total_time_label.configure(
            text=f"{duration_ms // 60000}:{(duration_ms // 1000) % 60:02}"
        )

    def _apply_update(info):
        (
            song_name,
            artists,
            album_art_url,
            progress_ms,
            duration_ms,
            track_id,
            playback_timestamp,
        ) = info

        if song_name:
            song_label.set_text(song_name)
        if artists:
            artist_label.set_text(artists)
        if album_art_url:
            album_label.set_image(album_art_url)

        if total_duration and progress_ms is not None:
            try:
                progress_bar.set((progress_ms or 0) / (duration_ms or 1))
            except Exception:
                pass

        p_ms = progress_ms or 0
        d_ms = duration_ms or 0

        current_time_label.configure(text=f"{p_ms // 60000}:{(p_ms // 1000) % 60:02}")
        total_time_label.configure(text=f"{d_ms // 60000}:{(d_ms // 1000) % 60:02}")

    def _poll_loop():
        while root.winfo_exists():
            try:
                info = get_current_song()
                # schedule GUI update on the main thread
                root.after(0, lambda i=info: _apply_update(i))
            except Exception:
                pass
            time.sleep(0.1)

    # start background polling thread only once
    if not getattr(root, "_polling_started", False):
        root._polling_started = True
        threading.Thread(target=_poll_loop, daemon=True).start()


def main():
    ctk.set_appearance_mode("dark")  # Set dark mode
    root = ctk.CTk()  # Using CustomTkinter's main window class
    root.title("Spotify Now Playing")

    elements = create_gui_elements(root)
    update_song_details(root, elements)
    root.mainloop()


if __name__ == "__main__":
    main()
