"""outfits app views — generate outfits and manage saved looks."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.engine.runner import generate_outfit
from apps.wardrobe.models import WardrobeItem
from .models import SavedLook
from .serializers import SavedLookSerializer, SaveLookCreateSerializer


# ── Outfit Generation ─────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_outfit_view(request):
    """
    Module 1 — Outfit Suggester.
    Run the 6-step engine on the user's wardrobe and return top 3 outfits.

    Request body:
        {
            "skin_tone":    int (1–7),
            "occasion":     str,
            "figure_type":  str (optional, default from profile),
        }
    """
    skin_tone = request.data.get("skin_tone")
    occasion = request.data.get("occasion", "casual")
    figure_type = request.data.get("figure_type", request.user.profile.figure_type)

    # Validate
    if skin_tone is None:
        return Response({"error": "skin_tone is required (1–7)."}, status=400)
    try:
        skin_tone = int(skin_tone)
        if not 1 <= skin_tone <= 7:
            raise ValueError
    except (ValueError, TypeError):
        return Response({"error": "skin_tone must be an integer between 1 and 7."}, status=400)

    valid_occasions = ["casual", "formal", "party", "sport", "ethnic_festive"]
    if occasion not in valid_occasions:
        return Response({"error": f"occasion must be one of: {', '.join(valid_occasions)}"}, status=400)

    # Save skin_tone preference to profile
    profile = request.user.profile
    profile.monk_scale = skin_tone
    profile.save(update_fields=["monk_scale"])

    # Handle optional Anchor Item
    anchor_item_id = request.data.get("anchor_item_id")
    anchor_item_dict = None
    if anchor_item_id:
        try:
            anchor_obj = WardrobeItem.objects.get(pk=anchor_item_id, user=request.user)
            anchor_item_dict = anchor_obj.to_engine_dict()
        except WardrobeItem.DoesNotExist:
            return Response({"error": "Anchor item not found."}, status=404)

    # Fetch wardrobe as engine dicts
    wardrobe_items = WardrobeItem.objects.filter(user=request.user, is_sample=False)
    wardrobe = [item.to_engine_dict() for item in wardrobe_items]

    # Run engine
    result = generate_outfit(
        wardrobe=wardrobe,
        skin_tone=skin_tone,
        occasion=occasion,
        figure_type=figure_type,
        anchor_item=anchor_item_dict,
    )

    return Response(result)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def style_me_view(request):
    """
    Module 2 — Style Me.
    Same engine but uses the curated sample dataset instead of personal wardrobe.
    No wardrobe upload needed — available to anonymous users.

    Request body: same as generate_outfit_view
    """
    skin_tone = request.data.get("skin_tone")
    occasion = request.data.get("occasion", "casual")

    # figure_type: use profile if logged in, otherwise default
    if request.user.is_authenticated:
        figure_type = request.data.get("figure_type", request.user.profile.figure_type)
        # Save skin_tone preference to profile
        profile = request.user.profile
        profile.monk_scale = int(skin_tone) if skin_tone else profile.monk_scale
        profile.save(update_fields=["monk_scale"])
    else:
        figure_type = request.data.get("figure_type", "average")

    try:
        skin_tone = int(skin_tone)
    except (TypeError, ValueError):
        return Response({"error": "skin_tone is required."}, status=400)

    result = generate_outfit(
        wardrobe=[],
        skin_tone=skin_tone,
        occasion=occasion,
        figure_type=figure_type,
        use_sample_only=True,
    )
    return Response(result)


# ── Saved Looks ───────────────────────────────────────────────────────────────

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def saved_looks_list(request):
    """
    GET  — list all saved looks for the user
    POST — save a generated look
    """
    if request.method == "GET":
        looks = SavedLook.objects.filter(user=request.user)
        serializer = SavedLookSerializer(looks, many=True)
        return Response({
            "looks": serializer.data,
            "count": looks.count(),
            "can_save_more": request.user.profile.can_save_look,
        })

    elif request.method == "POST":
        profile = request.user.profile

        # Tier check
        if not profile.can_save_look:
            return Response(
                {"error": "Free tier limit reached (3 saved looks). Upgrade to Premium for unlimited saves."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SaveLookCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        outfit_data = serializer.validated_data.get("outfit_data", {})
        occasion = serializer.validated_data.get("occasion", "casual")

        # Extract persona and score from outfit_data if available
        persona = outfit_data.get("persona", "")
        score = outfit_data.get("score", {})
        total_score = score.get("total", 0) if isinstance(score, dict) else 0

        look = SavedLook.objects.create(
            user=request.user,
            outfit_data=outfit_data,
            occasion=occasion,
            note=serializer.validated_data.get("note", ""),
            persona=persona,
            total_score=total_score,
        )
        return Response(SavedLookSerializer(look).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def saved_look_detail(request, pk):
    """GET or DELETE a specific saved look."""
    look = get_object_or_404(SavedLook, pk=pk, user=request.user)

    if request.method == "GET":
        return Response(SavedLookSerializer(look).data)

    elif request.method == "DELETE":
        look.delete()
        return Response({"message": "Look deleted."}, status=status.HTTP_204_NO_CONTENT)
