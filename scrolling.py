def scroll_text_independent(label, text, delay=150, pause_duration=1000):
    if hasattr(label, "scroll_after_id"):
        label.after_cancel(label.scroll_after_id)

    text = f"   {text}   "  # Add some space before and after the text
    max_visible_chars = int(label.winfo_width() / 10)  # Calculate based on width
    text_len = len(text)

    def scroll(index=0, direction=1):
        visible_text = text[index : index + max_visible_chars]
        label.configure(text=visible_text)

        if direction == 1 and index + max_visible_chars < text_len:
            index += 1
        elif direction == -1 and index > 0:
            index -= 1
        else:
            label.after(
                pause_duration, scroll, index, -direction
            )  # Pause and reverse direction
            return

        label.scroll_after_id = label.after(delay, scroll, index, direction)

    scroll()  # Start scrolling
