"""
Step 1 — Skin Tone → Colour Palette Mapping.

Input:  monk_scale (int, 1–7)
Output: dict with keys: flattering, neutrals, avoid (colour name lists)
"""
from .colour_data import MONK_SCALE_PALETTES


def get_skin_palette(monk_scale: int) -> dict:
    """
    Map a Monk Scale number to the user's personalised colour palette.

    Returns:
        {
            "flattering":     list[str],  # colour names that complement this tone
            "flattering_hex": list[str],  # corresponding hex values
            "neutrals":       list[str],  # safe anchor colours
            "neutrals_hex":   list[str],
            "avoid":          list[str],  # colours to exclude
            "avoid_hex":      list[str],
        }
    """
    scale = max(1, min(7, int(monk_scale)))
    return MONK_SCALE_PALETTES[scale]
