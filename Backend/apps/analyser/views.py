"""analyser app — Fashion Analyser views (Module 3)."""
import os
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from utils.hf_vision import analyse_outfit as analyse_outfit_hf
from utils.claude_vision import analyse_outfit_claude


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def analyse_outfit_view(request):
    """
    Module 3 — Fashion Analyser.
    Upload a full outfit photo and receive:
      - Letter grade (A / B / C / D)
      - What works well
      - 3 specific improvement tips

    Free tier: 3 uses per month. Premium: unlimited.
    """
    profile = request.user.profile

    # Tier check
    if not profile.can_use_analyser:
        return Response(
            {
                "error": "Monthly analysis limit reached (3 uses). Upgrade to Premium for unlimited Fashion Analyser.",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    image_file = request.FILES.get("image")
    if not image_file:
        return Response({"error": "An outfit image is required."}, status=400)

    # Save temporarily
    temp_path = default_storage.save(f"tmp/analyser/{image_file.name}", image_file)
    full_path = default_storage.path(temp_path)

    try:
        result = analyse_outfit_claude(full_path)
    except Exception as e:
        # Fallback to HF Vision gracefully if we hit rate limits / API key billing limits
        try:
            result = analyse_outfit_hf(full_path)
        except Exception as e:
            result = {
                "grade": "B",
                "works_well": "Analysis unavailable at this time.",
                "tips": [
                    "Ensure your outfit has a neutral anchor colour.",
                    "Keep formality consistent across all items.",
                    "Limit bold statement pieces to one per outfit.",
                ],
            }
    finally:
        # Clean up temp file
        try:
            os.remove(full_path)
        except Exception:
            pass

    # Increment usage counter
    profile.increment_analyser_uses()

    return Response({
        "grade": result.get("grade", "B"),
        "works_well": result.get("works_well", ""),
        "tips": result.get("tips", []),
        "analyser_uses_remaining": max(0, 3 - profile.analyser_uses_this_month)
        if profile.tier == "free" else "unlimited",
    })
