import tkinter as tk

import customtkinter as ctk


def _resolve_color(color):
    """Resolve a CustomTkinter color (which may be a tuple) to a tk-compatible value."""

    if isinstance(color, list) or isinstance(color, tuple):
        appearance = ctk.get_appearance_mode()
        return color[1] if appearance == "Dark" else color[0]
    return color


class SmoothScrollingLabel(ctk.CTkFrame):
    """A label-like widget that provides smooth marquee style scrolling."""

    def __init__(
        self,
        master,
        width,
        font,
        text_color="white",
        step=1,
        delay=15,
        pause=1000,
        **kwargs,
    ):
        super().__init__(master, width=width, fg_color="transparent", **kwargs)

        if isinstance(font, ctk.CTkFont):
            self._font = font
        elif isinstance(font, (tuple, list)):
            family = font[0] if len(font) > 0 else None
            size = font[1] if len(font) > 1 else None
            weight = font[2] if len(font) > 2 else None
            self._font = ctk.CTkFont(
                family=family,
                size=size,
                weight=weight,
            )
        else:
            self._font = ctk.CTkFont(font=font)
        self._text_color = text_color
        self._step = step
        self._delay = delay
        self._pause = pause
        self._current_text = ""
        self._scroll_job = None
        self._text_items = []
        self._gap = 40

        height = int(self._font.cget("size") * 2)
        self.configure(height=height)
        self.grid_propagate(False)
        self.pack_propagate(False)

        bg_color = _resolve_color(getattr(master, "cget", lambda _arg: "")("fg_color"))
        # print(_resolve_color(getattr(master, "cget", lambda _arg: "")("fg_color")))

        if not bg_color:
            bg_color = _resolve_color(self.cget("fg_color"))

        self._canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0,
            bg=bg_color,
        )
        self._canvas.pack(fill="both", expand=True)

        self.bind("<Configure>", self._handle_resize)

    def _handle_resize(self, event):
        if event.width == self._canvas.winfo_width():
            return
        self._canvas.configure(width=event.width)
        if self._current_text:
            # Re-render the text so that scrolling adapts to the new width.
            self.set_text(self._current_text, force=True)

    def _cancel_scroll(self):
        if self._scroll_job is not None:
            self.after_cancel(self._scroll_job)
            self._scroll_job = None

    def _start_scroll(self):
        self._scroll_job = self.after(self._delay, self._animate)

    def set_text(self, text, *, force=False):
        """Display new text, enabling smooth scrolling when necessary."""

        text = text or ""
        if not force and text == self._current_text:
            return

        self._current_text = text
        self._cancel_scroll()
        self._canvas.delete("all")
        self._text_items = []

        if not text:
            return

        center_y = self._canvas.winfo_height() // 2
        static_item = self._canvas.create_text(
            0,
            center_y,
            anchor="w",
            text=text,
            font=self._font,
            fill=self._text_color,
        )
        self._canvas.update_idletasks()
        bbox = self._canvas.bbox(static_item)
        text_width = (bbox[2] - bbox[0]) if bbox else 0
        canvas_width = self._canvas.winfo_width()

        if text_width <= canvas_width:
            return

        # Long text requires scrolling, so replace the static item with marquee items.
        self._canvas.delete(static_item)
        padded_text = f"{text}   "
        self._canvas.update_idletasks()
        first = self._canvas.create_text(
            0,
            center_y,
            anchor="w",
            text=padded_text,
            font=self._font,
            fill=self._text_color,
        )
        self._canvas.update_idletasks()
        bbox_first = self._canvas.bbox(first)
        text_width = (bbox_first[2] - bbox_first[0]) if bbox_first else text_width
        self._gap = max(40, canvas_width // 6)
        second = self._canvas.create_text(
            text_width + self._gap,
            center_y,
            anchor="w",
            text=padded_text,
            font=self._font,
            fill=self._text_color,
        )
        self._text_items = [first, second]
        self._scroll_job = self.after(self._pause, self._animate)

    def _animate(self):
        if not self._text_items:
            self._scroll_job = None
            return

        for item in self._text_items:
            self._canvas.move(item, -self._step, 0)

        canvas_width = self._canvas.winfo_width()
        center_y = self._canvas.winfo_height() // 2
        for idx, item in enumerate(self._text_items):
            bbox = self._canvas.bbox(item)
            if bbox and bbox[2] <= 0:
                other = self._text_items[(idx + 1) % len(self._text_items)]
                other_bbox = self._canvas.bbox(other)
                if other_bbox:
                    new_x = other_bbox[2] + self._gap
                else:
                    new_x = canvas_width
                self._canvas.coords(item, new_x, center_y)

        self._start_scroll()

    def clear(self):
        self.set_text("", force=True)
