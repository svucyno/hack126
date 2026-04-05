"""
Step 2 — Colour Harmony Filter.

Removes wardrobe items whose colour clashes with the user's skin tone palette.

Rules (item passes if ANY of these are true):
  1. Direct skin match  — item colour is in the flattering palette
  2. Harmonises        — complementary or analogous on the colour wheel
  3. Is a neutral      — white, black, grey, beige, camel etc.

Items failing all three are removed from the session wardrobe.
"""
from .colour_data import NEUTRAL_COLOURS, COLOUR_WHEEL_GROUPS


def _colour_group_index(colour_name: str) -> int | None:
    """Return the index of this colour's group on the wheel, or None."""
    colour_lower = colour_name.lower()
    for i, group in enumerate(COLOUR_WHEEL_GROUPS):
        if any(kw in colour_lower for kw in group):
            return i
    return None


def _is_neutral(colour_name: str) -> bool:
    colour_lower = colour_name.lower()
    return any(n in colour_lower for n in NEUTRAL_COLOURS)


def _is_neutral_hex(hex_colour: str) -> bool:
    """Check if a hex colour is visually close to neutral (low saturation)."""
    hex_colour = hex_colour.lstrip("#")
    try:
        r, g, b = int(hex_colour[0:2], 16), int(hex_colour[2:4], 16), int(hex_colour[4:6], 16)
    except (ValueError, IndexError):
        return True
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    saturation = (max_c - min_c) / max_c if max_c > 0 else 0
    return saturation < 0.15  # very low saturation = neutral-ish


def _complements(group_a: int, group_b: int, total: int = 7) -> bool:
    """Two colour groups are complementary if they are ~opposite on the wheel."""
    diff = abs(group_a - group_b)
    return diff == total // 2 or diff == (total // 2 + 1)


def _analogous(group_a: int, group_b: int, total: int = 7) -> bool:
    """Two colour groups are analogous if they are adjacent on the wheel."""
    diff = abs(group_a - group_b)
    return diff <= 1 or diff >= total - 1


def _item_passes_filter(item_colour_name: str, item_hex: str, palette: dict) -> tuple[bool, str]:
    """
    Test a single wardrobe item against the skin palette.

    Returns (passes: bool, reason: str)
    """
    colour_lower = item_colour_name.lower() if item_colour_name else ""

    # Rule 3 — Neutral anchor
    if _is_neutral(colour_lower) or _is_neutral_hex(item_hex):
        return True, "is_neutral"

    # Rule 1 — Direct skin palette match
    flattering = [c.lower() for c in palette.get("flattering", [])]
    if any(f in colour_lower or colour_lower in f for f in flattering):
        return True, "direct_skin_match"

    # Rule 2 — Colour wheel harmony with the flattering palette
    item_group = _colour_group_index(colour_lower)
    if item_group is not None:
        for flat_colour in flattering:
            flat_group = _colour_group_index(flat_colour)
            if flat_group is not None:
                if _complements(item_group, flat_group) or _analogous(item_group, flat_group):
                    return True, "harmonises_with_palette"

    return False, "no_harmony"


def filter_wardrobe(items: list[dict], palette: dict) -> list[dict]:
    """
    Filter a list of wardrobe item dicts against the skin palette.

    Each item dict must have:
        - colour_name: str  (e.g. "navy", "terracotta")
        - colour_hex:  str  (e.g. "#001f5b")
        (all other fields pass through unchanged)

    Returns filtered list with an added 'harmony_reason' field.
    """
    passed = []
    for item in items:
        colour_name = item.get("colour_name", "")
        colour_hex = item.get("colour_hex", "#808080")
        ok, reason = _item_passes_filter(colour_name, colour_hex, palette)
        if ok:
            item = dict(item)  # don't mutate original
            item["harmony_reason"] = reason
            passed.append(item)
    return passed


def check_outfit_pair_harmony(colour_a: str, colour_b: str) -> tuple[str, int]:
    """
    Check harmony between two item colours in a combination.

    Returns (harmony_type, score):
        complementary → 10 pts
        analogous     →  7 pts
        neutral_anchor→  8 pts
        weak          →  2 pts
    """
    if _is_neutral(colour_a) or _is_neutral(colour_b):
        return "neutral_anchor", 8

    group_a = _colour_group_index(colour_a)
    group_b = _colour_group_index(colour_b)

    if group_a is None or group_b is None:
        return "weak", 2
    if group_a == group_b:
        return "analogous", 7
    if _complements(group_a, group_b):
        return "complementary", 10
    if _analogous(group_a, group_b):
        return "analogous", 7
    return "weak", 2
