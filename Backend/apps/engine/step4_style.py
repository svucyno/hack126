"""
Step 4 — Style Layer: Persona Classification.

Stamps each outfit combination with one of six style personas.
Scoring uses four signals with defined weights:
  - Item types      35%
  - Pattern         25%
  - Formality avg   25%
  - Style tags      15%
"""
from .colour_data import (
    STYLE_PERSONAS,
    PERSONA_ITEM_TYPES,
    PERSONA_FORMALITY,
    PATTERN_WEIGHT,
)

PERSONA_PATTERNS = {
    "Ethnic Traditional": ["embroidered", "printed"],
    "Minimalist": ["solid"],
    "Casual Chic": ["solid", "striped"],
    "Boho": ["printed"],
    "Streetwear": ["graphic", "printed"],
    "Smart Formal": ["solid", "striped"],
}

PERSONA_OCCASIONS = {
    "Ethnic Traditional": "ethnic_festive",
    "Minimalist": "casual",
    "Casual Chic": "casual",
    "Boho": "casual",
    "Streetwear": "casual",
    "Smart Formal": "formal",
}


def _item_type_score(combo: dict, persona: str) -> float:
    """0–1 score based on how many item subtypes match the persona's expected types."""
    expected = [t.lower() for t in PERSONA_ITEM_TYPES.get(persona, [])]
    matches = 0
    total = 4
    for slot in ["top", "bottom", "shoes", "accessory"]:
        item = combo.get(slot, {})
        subtype = item.get("item_subtype", "").lower()
        item_type = item.get("item_type", "").lower()
        if any(e in subtype or e in item_type for e in expected):
            matches += 1
    return matches / total if total > 0 else 0


def _pattern_score(combo: dict, persona: str) -> float:
    """0–1 score based on pattern composition alignment."""
    expected_patterns = [p.lower() for p in PERSONA_PATTERNS.get(persona, [])]
    matches = 0
    total = 4
    for slot in ["top", "bottom", "shoes", "accessory"]:
        item = combo.get(slot, {})
        pattern = item.get("pattern", "solid").lower()
        if pattern in expected_patterns:
            matches += 1
    return matches / total if total > 0 else 0


def _formality_score(combo: dict, persona: str) -> float:
    """0–1 score based on whether average formality falls in the persona's expected range."""
    formalities = []
    for slot in ["top", "bottom", "shoes", "accessory"]:
        item = combo.get(slot, {})
        formalities.append(item.get("formality", 3))
    if not formalities:
        return 0
    avg_formality = sum(formalities) / len(formalities)
    min_f, max_f = PERSONA_FORMALITY.get(persona, (1, 5))
    if min_f <= avg_formality <= max_f:
        return 1.0
    distance = min(abs(avg_formality - min_f), abs(avg_formality - max_f))
    return max(0, 1 - distance / 3)


def classify_persona(combo: dict) -> tuple[str, float]:
    """
    Classify an outfit combination with a style persona.

    Args:
        combo: dict with keys 'top', 'bottom', 'shoes', 'accessory'

    Returns:
        (persona_name: str, confidence: float 0–1)
    """
    weights = {
        "item_type": 0.35,
        "pattern": 0.25,
        "formality": 0.25,
        "tags": 0.15,  # style tags (using pattern as proxy for now)
    }

    scores: dict[str, float] = {}
    for persona in STYLE_PERSONAS:
        item_type_sc = _item_type_score(combo, persona)
        pattern_sc = _pattern_score(combo, persona)
        formality_sc = _formality_score(combo, persona)
        tag_sc = pattern_sc  # proxy for style tags

        total = (
            weights["item_type"] * item_type_sc
            + weights["pattern"] * pattern_sc
            + weights["formality"] * formality_sc
            + weights["tags"] * tag_sc
        )
        scores[persona] = round(total, 4)

    best_persona = max(scores, key=scores.__getitem__)
    confidence = scores[best_persona]
    return best_persona, confidence
