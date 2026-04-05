"""
Step 3 — Combination Builder & Image Anchor.

Takes the filtered wardrobe and:
1. Separates items into their four slots: top, bottom, shoes, accessory
2. Fills any missing slot from the curated sample dataset
3. Generates every valid 4-piece combination for the chosen occasion
4. If an anchor item is provided, locks that slot and builds combinations around it
"""
from itertools import product as cartesian_product
from .colour_data import OCCASIONS
from .sample_dataset import SAMPLE_ITEMS


def _slot_items(items: list[dict], occasion: str) -> dict[str, list[dict]]:
    """
    Group items by slot type, keeping only those tagged for the chosen occasion.
    """
    slots: dict[str, list[dict]] = {"top": [], "bottom": [], "shoes": [], "accessory": []}
    for item in items:
        slot = item.get("item_type")
        if slot not in slots:
            continue
        item_occasions = item.get("occasions", [])
        if occasion in item_occasions or not item_occasions:
            slots[slot].append(item)
    return slots


def _fill_gaps(slots: dict, occasion: str, palette: dict) -> dict:
    """
    For any empty slot, pull matching items from the sample dataset.
    Marks filled items with 'is_sample': True.
    """
    from apps.engine.step2_filter import filter_wardrobe

    for slot in ["top", "bottom", "shoes", "accessory"]:
        if not slots[slot]:
            candidates = [
                item for item in SAMPLE_ITEMS
                if item.get("item_type") == slot
                and (occasion in item.get("occasions", []) or not item.get("occasions"))
            ]
            # Apply the same harmony filter to sample items
            if palette:
                candidates = filter_wardrobe(candidates, palette)
            slots[slot] = candidates[:5] or SAMPLE_ITEMS[:1]  # at worst: one item
    return slots


def build_combinations(
    filtered_items: list[dict],
    occasion: str,
    anchor_item: dict | None = None,
    palette: dict | None = None,
) -> list[dict]:
    """
    Build all valid 4-piece outfit combinations.

    Args:
        filtered_items: wardrobe items that passed Step 2
        occasion:       one of OCCASIONS
        anchor_item:    optional locked item (its slot is fixed)
        palette:        skin palette for gap-filling

    Returns:
        List of combination dicts, each containing:
        { "top": item, "bottom": item, "shoes": item, "accessory": item }
    """
    # Validate occasion
    if occasion not in OCCASIONS:
        occasion = "casual"

    slots = _slot_items(filtered_items, occasion)

    # If anchor is provided, lock its slot
    if anchor_item:
        anchor_slot = anchor_item.get("item_type", "top")
        if anchor_slot in slots:
            slots[anchor_slot] = [anchor_item]
            anchor_item["is_anchor"] = True

    # Fill missing slots from sample dataset
    slots = _fill_gaps(slots, occasion, palette or {})

    # Generate all combinations
    combinations = []
    for combo in cartesian_product(
        slots["top"], slots["bottom"], slots["shoes"], slots["accessory"]
    ):
        top, bottom, shoes, accessory = combo
        combinations.append({
            "top": top,
            "bottom": bottom,
            "shoes": shoes,
            "accessory": accessory,
        })

    return combinations
