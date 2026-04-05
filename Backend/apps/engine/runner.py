"""
Engine Runner — generate_outfit()

Chains all 6 steps in sequence and returns the top 3 outfits.

Usage:
    from apps.engine.runner import generate_outfit
    result = generate_outfit(
        wardrobe=list_of_item_dicts,
        skin_tone=4,
        occasion="ethnic_festive",
        anchor_item=None,
        figure_type="female",
    )
"""
from .step1_palette import get_skin_palette
from .step2_filter import filter_wardrobe
from .step3_builder import build_combinations
from .step4_style import classify_persona
from .step5_balancer import balance_check
from .step6_score import score_and_rank
from .sample_dataset import SAMPLE_ITEMS


def generate_outfit(
    wardrobe: list[dict],
    skin_tone: int,
    occasion: str,
    anchor_item: dict | None = None,
    figure_type: str = "female",
    use_sample_only: bool = False,
) -> dict:
    """
    Run the complete 6-step DripFit Colour Engine.

    Args:
        wardrobe:        List of wardrobe item dicts (from WardrobeItem model)
        skin_tone:       Monk Scale 1–7
        occasion:        One of: casual, formal, party, sport, ethnic_festive
        anchor_item:     Optional dict — item to lock as the anchor
        figure_type:     'female' | 'male' | 'neutral'
        use_sample_only: True for Module 2 (Style Me) — ignores personal wardrobe

    Returns:
        {
            "best_outfit":     {...},     # top-ranked outfit with full metadata
            "alternatives":    [{...}, {...}],
            "engine_stats":    {...},
            "error":           None | str,
        }
    """
    # ── Step 1: Skin Tone Palette ─────────────────────────────────────────────
    palette = get_skin_palette(skin_tone)

    # ── Source wardrobe ───────────────────────────────────────────────────────
    source = SAMPLE_ITEMS if use_sample_only else wardrobe

    # ── Step 2: Colour Harmony Filter ─────────────────────────────────────────
    filtered = filter_wardrobe(source, palette)

    stats = {
        "wardrobe_size": len(source),
        "after_filter": len(filtered),
        "combinations_built": 0,
        "after_balancer": 0,
        "rejection_rate": 0.0,
        "skin_tone": skin_tone,
        "occasion": occasion,
        "figure_type": figure_type,
    }

    if not filtered and not anchor_item:
        return {
            "best_outfit": None,
            "alternatives": [],
            "engine_stats": stats,
            "error": "No wardrobe items passed the colour harmony filter for this skin tone.",
        }

    # ── Step 3: Combination Builder ───────────────────────────────────────────
    combinations = build_combinations(
        filtered_items=filtered,
        occasion=occasion,
        anchor_item=anchor_item,
        palette=palette,
    )
    stats["combinations_built"] = len(combinations)

    if not combinations:
        return {
            "best_outfit": None,
            "alternatives": [],
            "engine_stats": stats,
            "error": "No valid outfit combinations could be built for this occasion.",
        }

    # ── Step 4 + 5: Style Layer + Balancer ───────────────────────────────────
    balanced_combos = []
    for combo in combinations:
        persona, confidence = classify_persona(combo)
        passes, balance_summary = balance_check(combo)

        if passes:
            balanced_combos.append({
                "combo": combo,
                "persona": persona,
                "persona_confidence": confidence,
                "balance_summary": balance_summary,
            })

    stats["after_balancer"] = len(balanced_combos)
    stats["rejection_rate"] = round(
        1 - (stats["after_balancer"] / stats["combinations_built"]), 3
    ) if stats["combinations_built"] > 0 else 0

    if not balanced_combos:
        # Relax and return best available without balancer
        # (graceful fallback — all outfits rejected is a bad UX)
        for combo in combinations[:3]:
            persona, confidence = classify_persona(combo)
            _, balance_summary = balance_check(combo)
            balanced_combos.append({
                "combo": combo,
                "persona": persona,
                "persona_confidence": confidence,
                "balance_summary": balance_summary,
            })

    # ── Step 6: Score & Rank ──────────────────────────────────────────────────
    top_3 = score_and_rank(balanced_combos, palette, occasion)

    def format_outfit(outfit_meta: dict) -> dict:
        combo = outfit_meta.get("combo", {})
        return {
            "items": {
                "top": combo.get("top", {}),
                "bottom": combo.get("bottom", {}),
                "shoes": combo.get("shoes", {}),
                "accessory": combo.get("accessory", {}),
            },
            "score": outfit_meta.get("score", {}),
            "persona": outfit_meta.get("persona", ""),
            "persona_confidence": outfit_meta.get("persona_confidence", 0),
            "balance_summary": outfit_meta.get("balance_summary", {}),
            "figure_type": figure_type,
            "palette": palette,
        }

    result = {
        "best_outfit": format_outfit(top_3[0]) if top_3 else None,
        "alternatives": [format_outfit(o) for o in top_3[1:]],
        "engine_stats": stats,
        "error": None,
    }
    return result
