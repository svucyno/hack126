"""
Utility: extract dominant colour from a clothing image using ColourThief.
Returns hex string like '#c4a882'.
"""
from colorthief import ColorThief
import io


def get_dominant_hex(image_path: str) -> str:
    """
    Extract the dominant colour from an image file.

    Args:
        image_path: Absolute path to the image file on disk.

    Returns:
        Hex colour string, e.g. '#c4a882'.
    """
    try:
        ct = ColorThief(image_path)
        rgb = ct.get_color(quality=1)  # (R, G, B)
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    except Exception:
        return "#808080"  # fallback neutral grey


def get_palette_hex(image_path: str, colour_count: int = 5) -> list[str]:
    """
    Extract a palette of dominant colours from an image.

    Returns a list of hex strings.
    """
    try:
        ct = ColorThief(image_path)
        palette = ct.get_palette(color_count=colour_count, quality=1)
        return ["#{:02x}{:02x}{:02x}".format(*rgb) for rgb in palette]
    except Exception:
        return ["#808080"]


def hex_to_rgb(hex_colour: str) -> tuple[int, int, int]:
    """Convert '#rrggbb' to (R, G, B)."""
    hex_colour = hex_colour.lstrip("#")
    return tuple(int(hex_colour[i : i + 2], 16) for i in (0, 2, 4))
