"""Entry point for ``python -m spotify_now_playing``."""

from .app import run_app


def main() -> None:
    """Launch the Spotify Now Playing desktop client."""

    run_app()


if __name__ == "__main__":
    main()
