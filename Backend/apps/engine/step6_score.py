"""
Step 6 — Score & Rank.

Every outfit surviving the Balancer is scored out of 100 across:
  - Colour Harmony   40pts  (how well the four colours work together)
  - Skin Tone Match  30pts  (how well each item flatters the skin tone — proximity matters)
  - Occasion Fit     30pts  (tag match + formality range check)

Top 3 outfits are returned.
"""
from .colour_data import OCCASION_FORMALITY
from .step2_filter import check_outfit_pair_harmony

# Slot weights for skin tone match (items closer to face weighted more)
SKIN_MATCH_WEIGHTS = {
    "top": 0.35,
    "accessory": 0.30,
    "bottom": 0.20,
    "shoes": 0.15,
}


def _colour_harmony_score(combo: dict) -> float:
    """
    Score colour harmony across all item pairs.
    6 pairs total (4 items = 6 combinations).
    Each pair scored: complementary=10, neutral=8, analogous=7, weak=2.
    Normalised to 40.
    """
    slots = ["top", "bottom", "shoes", "accessory"]
    pair_scores = []
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            a = combo[slots[i]].get("colour_name", "")
            b = combo[slots[j]].get("colour_name", "")
            _, score = check_outfit_pair_harmony(a, b)
            pair_scores.append(score)

    raw = sum(pair_scores)  # max possible: 6 * 10 = 60
    return round((raw / 60) * 40, 2)


def _skin_tone_score(combo: dict, palette: dict) -> float:
    """
    Score each item against the skin palette.
    Weighted by proximity to face.
    Direct match: 10pts, Harmony match: 7pts, Neutral: 5pts → normalised to 30.
    """
    flattering = [c.lower() for c in palette.get("flattering", [])]
    neutrals = [c.lower() for c in palette.get("neutrals", [])]

    weighted_score = 0.0
    for slot, weight in SKIN_MATCH_WEIGHTS.items():
        item = combo.get(slot, {})
        colour = item.get("colour_name", "").lower()

        # Direct palette match
        if any(f in colour or colour in f for f in flattering):
            pts = 10
        elif any(n in colour or colour in n for n in neutrals):
            pts = 5
        else:
            # Try harmony match via step2 filter
            from .step2_filter import _item_passes_filter
            ok, reason = _item_passes_filter(colour, item.get("colour_hex", "#808080"), palette)
            pts = 7 if ok and reason == "harmonises_with_palette" else 3

        weighted_score += weight * pts

    # weighted_score max = 1.0 * 10 = 10
    return round(weighted_score * 3, 2)  # scale to 30


def _occasion_fit_score(combo: dict, occasion: str) -> float:
    """
    Score 30pts total.
    Each item: 7.5pts max.
      Full:    tagged + formality in range  = 7.5
      Partial: tagged OR formality in range = 4
      Fail:    neither                      = 1
    """
    min_f, max_f = OCCASION_FORMALITY.get(occasion, (1, 5))
    total = 0.0
    slots = ["top", "bottom", "shoes", "accessory"]
    per_item_max = 30 / len(slots)

    for slot in slots:
        item = combo.get(slot, {})
        item_occasions = item.get("occasions", [])
        formality = item.get("formality", 3)
        tagged = occasion in item_occasions or not item_occasions
        formality_ok = min_f <= formality <= max_f

        if tagged and formality_ok:
            total += per_item_max
        elif tagged or formality_ok:
            total += per_item_max * 0.5
        else:
            total += per_item_max * (1 / 7.5)  # ~1 pt

    return round(total, 2)


def score_outfit(combo: dict, palette: dict, occasion: str) -> dict:
    """
    Score a single outfit combination.

    Returns a score dict with:
        total, colour_harmony, skin_tone_match, occasion_fit
    """
    harmony = _colour_harmony_score(combo)
    skin = _skin_tone_score(combo, palette)
    occasion_sc = _occasion_fit_score(combo, occasion)
    total = round(harmony + skin + occasion_sc, 1)

    return {
        "total": min(total, 100),
        "colour_harmony": harmony,
        "skin_tone_match": skin,
        "occasion_fit": occasion_sc,
    }


def score_and_rank(combos_with_meta: list[dict], palette: dict, occasion: str) -> list[dict]:
    """
    Score all combinations and return top 3, highest score first.

    Each combo_with_meta is expected to already have 'balance_summary' and 'persona' attached.

    Returns list of scored outfit dicts (max 3).
    """
    scored = []
    for combo_meta in combos_with_meta:
        combo = combo_meta.get("combo", combo_meta)
        score = score_outfit(combo, palette, occasion)
        scored.append({**combo_meta, "score": score})

    scored.sort(key=lambda x: x["score"]["total"], reverse=True)
    return scored[:3]
