"""
Claude Vision API Utility.

Uses Anthropic's Claude 3 Models (e.g. Sonnet) to:
1. analyse_item_claude()   → extract item metadata from a clothing photo
2. analyse_outfit_claude() → grade a full outfit photo (Fashion Analyser)
3. detect_skin_tone_claude() → estimate Monk Scale from a face/hand photo

This acts as the primary image analyzer. If it fails due to rate limits or 
billing issues, the system will fall back to `hf_vision.py`.
"""
import os
import base64
import json
import anthropic

# Initialize the Anthropic client. Make sure ANTHROPIC_API_KEY is in your .env
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
MODEL_NAME = "claude-3-5-sonnet-20240620"


def _encode_image(image_path: str) -> str:
    """Encode an image to base64 for Claude."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyse_item_claude(image_path: str) -> dict:
    """
    Analyse a clothing item image and return structured metadata.
    
    Returns:
        {
            "item_type": "top"|"bottom"|"shoes"|"accessory",
            "item_subtype": str,
            "pattern": str ("solid", "striped", "checked", "printed", "embroidered", "graphic"),
            "formality": int (1–5),
            "occasions": list[str] (e.g. ["casual", "formal", "party", "sport", "ethnic_festive"]),
            "caption": str,
        }
    """
    base64_image = _encode_image(image_path)

    prompt = """
    You are a fashion AI. Analyze the image of the clothing item or accessory.
    Output ONLY a valid JSON object with the following schema:
    {
        "item_type": "top" or "bottom" or "shoes" or "accessory",
        "item_subtype": "string (e.g., shirt, chinos, kurta, sneakers, watch)",
        "pattern": "solid", "striped", "checked", "printed", "embroidered", or "graphic",
        "formality": integer from 1 (very casual) to 5 (very formal),
        "occasions": list of strings chosen from: ["casual", "formal", "party", "sport", "ethnic_festive"],
        "caption": "A concise 1-sentence description of the item"
    }
    Make sure your response contains nothing but the JSON object.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",  # Anthropic accepts jpeg, png, webp. Standardizing content type for prompt is fine for most common image files
                            "data": base64_image,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    try:
        response_text = response.content[0].text
        # Fallback cleanup just in case there are markdown ticks
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        
        return json.loads(response_text)
    except Exception as e:
        raise RuntimeError("Failed to parse Claude Vision output for item analysis.") from e


def analyse_outfit_claude(image_path: str) -> dict:
    """
    Analyse a full outfit photo and return a critique.
    
    Returns:
        {
            "grade": "A"|"B"|"C"|"D",
            "works_well": str,
            "tips": [str, str, str],
        }
    """
    base64_image = _encode_image(image_path)

    prompt = """
    You are a fashion stylist AI grading a full outfit.
    Provide a critique by evaluating color harmony, visual balance, formality consistency, and occasion suitability.
    Output ONLY a valid JSON object with the following schema:
    {
        "grade": "A" or "B" or "C" or "D",
        "works_well": "A 1-2 sentence description of what looks good in this outfit",
        "tips": ["Tip 1", "Tip 2", "Tip 3"] (Exactly 3 specific, actionable improvement tips)
    }
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    try:
        response_text = response.content[0].text
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
            
        return json.loads(response_text)
    except Exception as e:
        raise RuntimeError("Failed to parse Claude Vision output for outfit critique.") from e


def detect_skin_tone_claude(image_path: str) -> int:
    """
    Estimate Monk Scale (1–7) from a photo.
    Returns an integer 1–7.
    """
    base64_image = _encode_image(image_path)

    prompt = """
    Analyze the skin tone of the person in the photo. 
    Map it to the Monk Skin Tone Scale, simplified here as an integer from 1 (very light/fair) to 7 (very deep/dark).
    Output ONLY a valid JSON object with the following schema:
    {
        "monk_scale": integer between 1 and 7
    }
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    try:
        response_text = response.content[0].text
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
            
        result = json.loads(response_text)
        return int(result.get("monk_scale", 3))
    except Exception as e:
        raise RuntimeError("Failed to parse Claude Vision output for skin tone detection.") from e
