"""wardrobe app views."""
import os
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import WardrobeItem
from .serializers import WardrobeItemSerializer, WardrobeItemUploadSerializer, WardrobeItemEditSerializer
from utils.colour_thief import get_dominant_hex
from utils.hf_vision import analyse_item as analyse_item_hf
from utils.claude_vision import analyse_item_claude
from utils.image_processing import remove_background, REMBG_AVAILABLE
import datetime


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wardrobe_list(request):
    """List all wardrobe items for the authenticated user."""
    items = WardrobeItem.objects.filter(user=request.user, is_sample=False)
    serializer = WardrobeItemSerializer(items, many=True, context={"request": request})
    return Response({
        "items": serializer.data,
        "count": items.count(),
        "tier": request.user.profile.tier,
        "can_upload_more": request.user.profile.can_upload_wardrobe_item,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def wardrobe_upload(request):
    """
    Upload a clothing item photo.
    Auto-analyses with ColourThief + Claude (fallback to HF) and stores metadata.
    Also removes background for the Anchor Feature.
    """
    profile = request.user.profile

    # Tier check
    if not profile.can_upload_wardrobe_item:
        return Response(
            {"error": "Free tier limit reached (10 items). Upgrade to Premium for unlimited wardrobe."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = WardrobeItemUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Save image first so we have a path
    item = serializer.save(user=request.user)

    image_path = item.image.path

    # Extract dominant colour with ColourThief
    try:
        item.colour_hex = get_dominant_hex(image_path)
    except Exception:
        item.colour_hex = "#808080"

    # Background Removal for the Anchor Feature
    if REMBG_AVAILABLE:
        try:
            filename = os.path.basename(image_path)
            name, _ = os.path.splitext(filename)
            cutout_filename = f"{name}_cutout.png"
            
            # Construct absolute paths
            base_upload_dir = os.path.dirname(image_path)
            cutouts_dir = os.path.join(base_upload_dir, "cutouts")
            cutout_abs_path = os.path.join(cutouts_dir, cutout_filename)
            
            # Process via utils
            remove_background(image_path, cutout_abs_path)
            
            # Build relative path for Django ImageField (e.g., wardrobe/cutouts/2026/04/file_cutout.png)
            now = datetime.datetime.now()
            # Find the media relative prefix, assuming standard pattern
            rel_path = f"wardrobe/cutouts/{now.strftime('%Y/%m')}/{cutout_filename}"
            item.cutout_image.name = rel_path
        except Exception:
            pass # Fallback: Anchor slot will just rendering the original or fallback colour

    # Analyse with Claude Vision
    try:
        metadata = analyse_item_claude(image_path)
    except Exception as e:
        # Fallback to Hugging Face Vision safely if Claude rejects (e.g. rate limit / billing cap)
        try:
            metadata = analyse_item_hf(image_path)
        except Exception:
            metadata = {}
            
    try:
        item.item_type = metadata.get("item_type", "top")
        item.item_subtype = metadata.get("item_subtype", "")
        item.pattern = metadata.get("pattern", "solid")
        item.formality = metadata.get("formality", 3)
        item.occasions = metadata.get("occasions", ["casual"])
        item.caption = metadata.get("caption", "")
    except Exception as e:
        # Gracefully degrade — item saved with defaults
        pass

    item.save()

    return Response(
        WardrobeItemSerializer(item, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def wardrobe_item_detail(request, pk):
    """Retrieve, update metadata, or delete a wardrobe item."""
    item = get_object_or_404(WardrobeItem, pk=pk, user=request.user)

    if request.method == "GET":
        serializer = WardrobeItemSerializer(item, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PATCH":
        # Manual metadata edit (REQ-W07)
        serializer = WardrobeItemEditSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(WardrobeItemSerializer(item, context={"request": request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # Remove image file too
        try:
            if item.image and os.path.isfile(item.image.path):
                os.remove(item.image.path)
        except Exception:
            pass
        item.delete()
        return Response({"message": "Item deleted."}, status=status.HTTP_204_NO_CONTENT)
