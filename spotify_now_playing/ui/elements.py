"""Utilities for constructing the CustomTkinter interface."""

from __future__ import annotations

from dataclasses import dataclass

import customtkinter as ctk

from .widgets import AlbumLabel, SmoothScrollingLabel

__all__ = ["SongDisplayWidgets", "build_ui"]


@dataclass(frozen=True)
class SongDisplayWidgets:
    """Convenience container for the widgets used to render track details."""

    song_label: SmoothScrollingLabel
    artist_label: SmoothScrollingLabel
    album_label: AlbumLabel
    progress_bar: ctk.CTkProgressBar
    current_time_label: ctk.CTkLabel
    total_time_label: ctk.CTkLabel


def build_ui(root: ctk.CTk) -> SongDisplayWidgets:
    """Create the GUI hierarchy for the application."""

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

    return SongDisplayWidgets(
        song_label=song_label,
        artist_label=artist_label,
        album_label=album_label,
        progress_bar=progress_bar,
        current_time_label=current_time_label,
        total_time_label=total_time_label,
    )
