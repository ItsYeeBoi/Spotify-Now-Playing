"""Reusable CustomTkinter widgets used across the application."""

from __future__ import annotations

import tkinter as tk
from io import BytesIO
from typing import Iterable, Tuple

import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageOps

__all__ = ["AlbumLabel", "SmoothScrollingLabel"]


def _resolve_color(color: object) -> str:
    """Resolve a CustomTkinter color to a value understood by Tk."""

    if isinstance(color, (list, tuple)):
        appearance = ctk.get_appearance_mode()
        return color[1] if appearance == "Dark" and len(color) > 1 else color[0]
    return str(color)


class AlbumLabel(ctk.CTkLabel):
    """Label capable of downloading and displaying album artwork."""

    _size: Tuple[int, int] = (100, 100)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.image_url: str | None = None
        self._image: ctk.CTkImage | None = None

    def set_image(self, url: str | None) -> None:
        """Download and display the image located at ``url``."""

        if not url:
            self.clear()
            return

        if self.image_url == url:
            return

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.resize(self._size, Image.LANCZOS)
        img = self._rounded_image(img, radius=5)

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=self._size)
        self.configure(image=ctk_img, text="")
        self.image_url = url
        self._image = ctk_img

    def clear(self) -> None:
        """Remove the currently displayed album artwork."""

        self.configure(image=None, text="")
        self._label.configure(image="")

        self.image_url = None
        self._image = None

    @staticmethod
    def _rounded_image(image: Image.Image, radius: int) -> Image.Image:
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)
        rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        rounded_image.putalpha(mask)
        return rounded_image


class SmoothScrollingLabel(ctk.CTkFrame):
    """A label-like widget that provides smooth marquee-style scrolling."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        width: int,
        font: ctk.CTkFont | Iterable[str | int] | str,
        text_color: str = "white",
        step: int = 1,
        delay: int = 15,
        pause: int = 1000,
        **kwargs: object,
    ) -> None:
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
        self._scroll_job: str | None = None
        self._text_items: list[int] = []
        self._gap = 40

        height = int(self._font.cget("size") * 2)
        self.configure(height=height)
        self.grid_propagate(False)
        self.pack_propagate(False)

        bg_color = _resolve_color(getattr(master, "cget", lambda _arg: "")("fg_color"))
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

    def _handle_resize(self, event: tk.Event[tk.Misc]) -> None:
        if event.width == self._canvas.winfo_width():
            return
        self._canvas.configure(width=event.width)
        if self._current_text:
            self.set_text(self._current_text, force=True)

    def _cancel_scroll(self) -> None:
        if self._scroll_job is not None:
            self.after_cancel(self._scroll_job)
            self._scroll_job = None

    def _start_scroll(self) -> None:
        self._scroll_job = self.after(self._delay, self._animate)

    def set_text(self, text: str | None, *, force: bool = False) -> None:
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

    def _animate(self) -> None:
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
                new_x = (other_bbox[2] + self._gap) if other_bbox else canvas_width
                self._canvas.coords(item, new_x, center_y)

        self._start_scroll()

    def clear(self) -> None:
        self.set_text("", force=True)
