"""
Hugging Face Vision utility.

Uses the HF Inference API to:
1. analyse_item()   → extract item metadata from a clothing photo
2. analyse_outfit() → grade a full outfit photo (Fashion Analyser)
3. detect_skin_tone() → estimate Monk Scale from a face/hand photo
"""
import os
import base64
import json
import requests
from pathlib import Path

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
HF_VISION_MODEL = os.getenv("HF_VISION_MODEL", "Salesforce/blip-image-captioning-large")

# We use the free BLIP captioning model for item description,
# then parse the caption with rule-based logic.
BLIP_API_URL = f"https://api-inference.huggingface.co/models/{HF_VISION_MODEL}"

# For outfit grading we use a zero-shot classification approach
ZSC_MODEL = "facebook/bart-large-mnli"
ZSC_API_URL = f"https://api-inference.huggingface.co/models/{ZSC_MODEL}"

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}


def _image_to_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def _caption_image(image_path: str) -> str:
    """Get BLIP caption for an image. Returns raw caption string."""
    try:
        data = _image_to_bytes(image_path)
        response = requests.post(BLIP_API_URL, headers=HEADERS, data=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and result:
            return result[0].get("generated_text", "")
        return ""
    except Exception as e:
        return ""


def _classify_text(text: str, candidate_labels: list[str]) -> dict:
    """Zero-shot classify text using BART MNLI."""
    try:
        payload = {"inputs": text, "parameters": {"candidate_labels": candidate_labels}}
        response = requests.post(ZSC_API_URL, headers=HEADERS, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

ITEM_TYPE_KEYWORDS = {
    "top": ["shirt", "blouse", "top", "kurta", "t-shirt", "sweatshirt", "jacket", "hoodie", "tee"],
    "bottom": ["jeans", "trousers", "skirt", "shorts", "churidar", "palazzos", "pants", "jogger"],
    "shoes": ["shoes", "sneakers", "heels", "boots", "loafers", "flats", "juttis", "sandals", "footwear"],
    "accessory": ["bag", "watch", "belt", "scarf", "dupatta", "jewellery", "necklace", "bracelet", "cap", "hat"],
}

PATTERN_KEYWORDS = {
    "graphic": ["graphic", "print", "logo"],
    "embroidered": ["embroidered", "embroidery"],
    "printed": ["printed", "pattern", "floral", "tie-dye"],
    "striped": ["striped", "stripe"],
    "checked": ["checked", "check", "plaid"],
    "solid": ["plain", "solid", "single colour", "one color"],
}

SUBTYPE_MAP = {
    "top": {
        "kurta": ["kurta"],
        "hoodie": ["hoodie", "sweatshirt"],
        "blouse": ["blouse"],
        "t-shirt": ["t-shirt", "tee"],
        "shirt": ["shirt"],
        "jacket": ["jacket"],
    },
    "bottom": {
        "churidar": ["churidar"],
        "palazzos": ["palazzo"],
        "jeans": ["jeans", "denim"],
        "trousers": ["trouser", "chino", "pant"],
        "skirt": ["skirt"],
        "shorts": ["short"],
        "joggers": ["jogger"],
    },
    "shoes": {
        "juttis": ["jutti"],
        "sneakers": ["sneaker", "trainer"],
        "heels": ["heel"],
        "boots": ["boot"],
        "loafers": ["loafer"],
        "flats": ["flat", "sandal"],
    },
    "accessory": {
        "dupatta": ["dupatta"],
        "bag": ["bag", "handbag", "purse"],
        "watch": ["watch"],
        "belt": ["belt"],
        "scarf": ["scarf"],
        "jewellery": ["jewellery", "jewelry", "necklace", "bracelet", "ring"],
    },
}

OCCASION_KEYWORDS = {
    "casual": ["casual", "everyday", "relaxed", "jeans", "t-shirt", "sneaker"],
    "formal": ["formal", "office", "professional", "blazer", "suit"],
    "party": ["party", "night out", "festive", "glam"],
    "sport": ["sport", "gym", "athletic", "activewear", "jogger"],
    "ethnic_festive": ["ethnic", "kurta", "churidar", "dupatta", "jutti", "festive", "traditional", "indian"],
}


def _detect_item_type(caption: str) -> str:
    caption_lower = caption.lower()
    for item_type, keywords in ITEM_TYPE_KEYWORDS.items():
        if any(kw in caption_lower for kw in keywords):
            return item_type
    return "top"  # safe default


def _detect_subtype(item_type: str, caption: str) -> str:
    caption_lower = caption.lower()
    subtypes = SUBTYPE_MAP.get(item_type, {})
    for subtype, keywords in subtypes.items():
        if any(kw in caption_lower for kw in keywords):
            return subtype
    return item_type  # fallback


def _detect_pattern(caption: str) -> str:
    caption_lower = caption.lower()
    for pattern, keywords in PATTERN_KEYWORDS.items():
        if any(kw in caption_lower for kw in keywords):
            return pattern
    return "solid"  # default


def _estimate_formality(item_type: str, subtype: str, pattern: str) -> int:
    formal_items = {"blazer", "dress shoes", "heels", "trousers", "formal shirt"}
    casual_items = {"t-shirt", "sneakers", "shorts", "hoodie", "joggers"}
    ethnic_items = {"kurta", "churidar", "dupatta", "juttis", "palazzos"}
    if subtype in formal_items:
        return 4
    if subtype in ethnic_items:
        return 3
    if subtype in casual_items:
        return 2
    if pattern == "graphic":
        return 2
    if item_type == "shoes" and subtype in {"heels", "loafers"}:
        return 4
    return 3  # smart-casual default


def _detect_occasions(item_type: str, subtype: str, pattern: str, formality: int) -> list[str]:
    occasions = []
    if subtype in ["kurta", "churidar", "dupatta", "juttis", "palazzos"]:
        occasions.append("ethnic_festive")
    if formality <= 2:
        occasions.extend(["casual", "sport"])
    if formality in [2, 3]:
        occasions.append("casual")
    if formality in [3, 4]:
        occasions.append("party")
    if formality >= 4:
        occasions.append("formal")
    return list(set(occasions)) or ["casual"]


def analyse_item(image_path: str) -> dict:
    """
    Analyse a clothing item image and return structured metadata.

    Returns:
        {
            "item_type": "top"|"bottom"|"shoes"|"accessory",
            "item_subtype": str,
            "pattern": str,
            "formality": int (1–5),
            "occasions": list[str],
            "caption": str,
        }
    """
    caption = _caption_image(image_path)

    if not caption:
        # HF token missing or model unavailable — return safe defaults
        return {
            "item_type": "top",
            "item_subtype": "shirt",
            "pattern": "solid",
            "formality": 3,
            "occasions": ["casual"],
            "caption": "",
        }

    item_type = _detect_item_type(caption)
    subtype = _detect_subtype(item_type, caption)
    pattern = _detect_pattern(caption)
    formality = _estimate_formality(item_type, subtype, pattern)
    occasions = _detect_occasions(item_type, subtype, pattern, formality)

    return {
        "item_type": item_type,
        "item_subtype": subtype,
        "pattern": pattern,
        "formality": formality,
        "occasions": occasions,
        "caption": caption,
    }


def analyse_outfit(image_path: str) -> dict:
    """
    Analyse a full outfit photo and return a critique.

    Returns:
        {
            "grade": "A"|"B"|"C"|"D",
            "works_well": str,
            "tips": [str, str, str],
        }
    """
    caption = _caption_image(image_path)

    if not caption:
        return {
            "grade": "B",
            "works_well": "Unable to analyse image — please ensure Hugging Face API token is configured.",
            "tips": [
                "Ensure your outfit includes a neutral anchor colour.",
                "Check that formality levels are consistent across all items.",
                "Limit bold/printed items to one per outfit.",
            ],
        }

    # Grade via zero-shot classification on the caption
    grade_labels = [
        "excellent outfit, very well coordinated",
        "good outfit, mostly coordinated",
        "average outfit, needs some improvement",
        "poor outfit, significant style issues",
    ]
    zsc_result = _classify_text(caption, grade_labels)

    grade = "B"  # default
    if zsc_result and "labels" in zsc_result:
        top_label = zsc_result["labels"][0]
        grade_map = {
            "excellent outfit, very well coordinated": "A",
            "good outfit, mostly coordinated": "B",
            "average outfit, needs some improvement": "C",
            "poor outfit, significant style issues": "D",
        }
        grade = grade_map.get(top_label, "B")

    # Generate tips based on caption analysis
    tips = []
    caption_lower = caption.lower()

    if "bright" in caption_lower or "colourful" in caption_lower:
        tips.append("Consider adding a neutral anchor (white, black, or beige) to balance the bold colours.")
    if len(tips) < 3:
        tips.append("Ensure all items share a similar formality level to create a cohesive look.")
    if len(tips) < 3:
        tips.append("Try adding an accessory near the face — it elevates the outfit significantly.")
    if len(tips) < 3:
        tips.append("Check that your shoe choice complements the formality of the rest of the outfit.")

    return {
        "grade": grade,
        "works_well": f"The outfit features: {caption}",
        "tips": tips[:3],
    }


def detect_skin_tone(image_path: str) -> int:
    """
    Estimate Monk Scale (1–7) from a face or hand photo.
    Uses average pixel brightness as a proxy (simplified approach without ML model).
    Returns an integer 1–7.
    """
    try:
        from PIL import Image
        import numpy as np

        img = Image.open(image_path).convert("RGB")
        img_small = img.resize((100, 100))
        pixels = list(img_small.getdata())
        avg_r = sum(p[0] for p in pixels) / len(pixels)
        avg_g = sum(p[1] for p in pixels) / len(pixels)
        avg_b = sum(p[2] for p in pixels) / len(pixels)
        brightness = (avg_r + avg_g + avg_b) / 3

        # Map brightness (0–255) to Monk scale (1=lightest, 7=darkest)
        if brightness > 220:
            return 1
        elif brightness > 190:
            return 2
        elif brightness > 160:
            return 3
        elif brightness > 130:
            return 4
        elif brightness > 100:
            return 5
        elif brightness > 70:
            return 6
        else:
            return 7
    except Exception:
        return 3  # default mid-tone
