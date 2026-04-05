"""
Step 5 — Outfit Balancer.

Quality gate that rejects combinations with:
  Rule 1 — More than 1 bold item (visual weight ≥ 4)
  Rule 2 — Any two items more than 1 formality level apart

Items that fail are excluded from scoring.
"""
from .colour_data import PATTERN_WEIGHT


def _visual_weight(item: dict) -> int:
    """
    Calculate visual weight of a single item.

    Pattern base weight + colour impact modifier:
      solid=1, striped/checked=2, printed/embroidered/graphic=3
      Muted/neutral: +0, Moderate: +1, Vivid/saturated: +2

    Bold threshold: total weight ≥ 4
    """
    pattern = item.get("pattern", "solid").lower()
    base = PATTERN_WEIGHT.get(pattern, 1)

    # Estimate colour impact from hex saturation
    hex_colour = item.get("colour_hex", "#808080").lstrip("#")
    try:
        r, g, b = int(hex_colour[0:2], 16), int(hex_colour[2:4], 16), int(hex_colour[4:6], 16)
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        saturation = (max_c - min_c) / max_c if max_c > 0 else 0
        if saturation < 0.2:
            colour_impact = 0
        elif saturation < 0.5:
            colour_impact = 1
        else:
            colour_impact = 2
    except (ValueError, IndexError):
        colour_impact = 0

    return base + colour_impact


def _count_bold_items(combo: dict) -> tuple[int, list[str]]:
    """Return count of bold items and which slots they are."""
    bold_slots = []
    for slot in ["top", "bottom", "shoes", "accessory"]:
        item = combo.get(slot, {})
        if _visual_weight(item) >= 4:
            bold_slots.append(slot)
    return len(bold_slots), bold_slots


def _formality_gap_ok(combo: dict) -> tuple[bool, int]:
    """
    Check that no two items are more than 1 formality level apart.
    Returns (passes: bool, max_gap: int)
    """
    formalities = []
    for slot in ["top", "bottom", "shoes", "accessory"]:
        item = combo.get(slot, {})
        formalities.append(item.get("formality", 3))

    max_gap = 0
    for i in range(len(formalities)):
        for j in range(i + 1, len(formalities)):
            gap = abs(formalities[i] - formalities[j])
            max_gap = max(max_gap, gap)

    return max_gap <= 1, max_gap


def balance_check(combo: dict) -> tuple[bool, dict]:
    """
    Run both balance rules on an outfit combination.

    Returns:
        (passes: bool, balance_summary: dict)
    """
    bold_count, bold_slots = _count_bold_items(combo)
    formality_ok, max_gap = _formality_gap_ok(combo)

    passes = bold_count <= 1 and formality_ok

    # Identify the statement piece (the bold item, if exactly one)
    statement_piece = bold_slots[0] if bold_count == 1 else None

    # Average formality
    formalities = [combo[s].get("formality", 3) for s in ["top", "bottom", "shoes", "accessory"]]
    avg_formality = round(sum(formalities) / len(formalities), 1)

    summary = {
        "passes": passes,
        "bold_item_count": bold_count,
        "bold_slots": bold_slots,
        "statement_piece": statement_piece,
        "formality_gap": max_gap,
        "average_formality": avg_formality,
        "reject_reason": (
            None if passes else
            "too_many_bold_items" if bold_count > 1 else
            "formality_gap_too_large"
        ),
    }
    return passes, summary
