def scroll_text_synchronized(
    song_label, artist_label, song_text, artist_text, delay=150, pause_duration=1000
):
    # Add markers to the start and end of the text for debugging (optional)
    song_text = f"|{song_text}|"
    artist_text = f"|{artist_text}|"

    # Calculate the maximum visible characters for each label
    max_song_visible_chars = song_label.cget("width")
    max_artist_visible_chars = artist_label.cget("width")

    song_len = len(song_text)
    artist_len = len(artist_text)

    # Determine the max length for scrolling
    max_scroll_length = max(song_len, artist_len)

    def scroll(index=0, direction=1, song_finished=False, artist_finished=False):
        # Determine visible text for both song and artist
        song_visible_text = song_text[index : index + max_song_visible_chars]
        artist_visible_text = artist_text[index : index + max_artist_visible_chars]

        # Update the labels
        song_label.configure(text=song_visible_text)
        artist_label.configure(text=artist_visible_text)

        # Check if either label has reached the end
        if direction == 1:  # Moving forward
            if index + max_song_visible_chars < song_len:
                index += 1
            else:
                song_finished = True

            if index + max_artist_visible_chars < artist_len:
                index += 1
            else:
                artist_finished = True

            # If both have finished, pause and reverse direction
            if song_finished and artist_finished:
                song_label.after(pause_duration, scroll, index, -1)
                return

        else:  # Moving backward
            if index > 0:
                index -= 1
            else:  # Reached the start, pause and move forward again
                song_label.after(pause_duration, scroll, index, 1)
                return

        # Continue scrolling
        song_label.after(
            delay, scroll, index, direction, song_finished, artist_finished
        )

    scroll()  # Start synchronized scrolling
