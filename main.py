import customtkinter as ctk
from gui_elements import create_gui_elements
from scrolling import scroll_text_independent
from spotify_api import get_current_song

# Global variables to track the current song and artist
current_song_name = None
current_artist_name = None


def update_song_details(root, elements):
    global current_song_name, current_artist_name
    (
        song_label,
        artist_label,
        album_label,
        progress_bar,
        current_time_label,
        total_time_label,
    ) = elements

    song_name, artists, album_art_url, progress_ms, duration_ms, _ = get_current_song()

    if song_name:
        if song_name != current_song_name:
            current_song_name = song_name
            if hasattr(song_label, "scroll_after_id"):
                song_label.after_cancel(song_label.scroll_after_id)
            song_label.configure(text=song_name)
            if (
                len(song_name) * 10 > song_label.winfo_width()
            ):  # Check if scrolling is needed
                scroll_text_independent(song_label, song_name)

        if artists != current_artist_name:
            current_artist_name = artists
            if hasattr(artist_label, "scroll_after_id"):
                artist_label.after_cancel(artist_label.scroll_after_id)
            artist_label.configure(text=artists)
            if (
                len(artists) * 10 > artist_label.winfo_width()
            ):  # Check if scrolling is needed
                scroll_text_independent(artist_label, artists)

        if album_art_url:
            album_label.set_image(album_art_url)

        progress_bar.set(progress_ms / duration_ms)
        current_time_label.configure(
            text=f"{progress_ms // 60000}:{(progress_ms // 1000) % 60:02}"
        )
        total_time_label.configure(
            text=f"{duration_ms // 60000}:{(duration_ms // 1000) % 60:02}"
        )

    root.after(100, update_song_details, root, elements)


def main():
    ctk.set_appearance_mode("dark")  # Set dark mode
    root = ctk.CTk()  # Using CustomTkinter's main window class
    root.title("Spotify Now Playing")

    elements = create_gui_elements(root)
    update_song_details(root, elements)
    root.mainloop()


if __name__ == "__main__":
    main()
