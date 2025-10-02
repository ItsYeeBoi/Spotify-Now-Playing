from io import BytesIO

import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageOps

from scrolling import SmoothScrollingLabel


class AlbumLabel(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_url = None

    def set_image(self, url):
        if self.image_url == url:
            return

        self.image_url = url
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        img = img.resize((100, 100), Image.LANCZOS)
        img = self.rounded_image(img, radius=15)

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))
        self.configure(image=ctk_img, text="")
        self.image = ctk_img

    def rounded_image(self, image, radius):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)
        rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        rounded_image.putalpha(mask)
        return rounded_image


def create_gui_elements(root):
    root.geometry("500x200")

    main_frame = ctk.CTkFrame(root, corner_radius=10)
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    album_label = AlbumLabel(main_frame)
    album_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="n")

    details_frame = ctk.CTkFrame(main_frame, corner_radius=15)
    details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

    label_width = 300

    song_label = SmoothScrollingLabel(
        details_frame,
        width=label_width,
        font=("Helvetica", 16),
        text_color="white",
    )
    song_label.pack(pady=5, padx=10, fill="x")

    artist_label = SmoothScrollingLabel(
        details_frame,
        width=label_width,
        font=("Helvetica", 12),
        text_color="gray",
    )
    artist_label.pack(pady=5, padx=10, fill="x")

    progress_frame = ctk.CTkFrame(main_frame, corner_radius=15)
    progress_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    current_time_label = ctk.CTkLabel(
        progress_frame, text="0:00", font=("Helvetica", 10), text_color="white"
    )
    current_time_label.pack(side="left", padx=(10, 5))

    progress_bar = ctk.CTkProgressBar(
        progress_frame, width=250, height=10, corner_radius=5
    )
    progress_bar.pack(side="left", padx=10, pady=5)

    total_time_label = ctk.CTkLabel(
        progress_frame, text="0:00", font=("Helvetica", 10), text_color="white"
    )
    total_time_label.pack(side="left", padx=(5, 10))

    return (
        song_label,
        artist_label,
        album_label,
        progress_bar,
        current_time_label,
        total_time_label,
    )
