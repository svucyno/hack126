"""wardrobe app serializers."""
from rest_framework import serializers
from .models import WardrobeItem


class WardrobeItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = WardrobeItem
        fields = [
            "id",
            "image_url",
            "colour_hex",
            "colour_name",
            "item_type",
            "item_subtype",
            "pattern",
            "formality",
            "occasions",
            "is_sample",
            "caption",
            "created_at",
        ]
        read_only_fields = ["id", "image_url", "created_at", "is_sample"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class WardrobeItemUploadSerializer(serializers.ModelSerializer):
    """Serializer for the initial upload — only requires image."""

    class Meta:
        model = WardrobeItem
        fields = ["image"]


class WardrobeItemEditSerializer(serializers.ModelSerializer):
    """Serializer for manual metadata editing (REQ-W07)."""

    class Meta:
        model = WardrobeItem
        fields = [
            "colour_name",
            "item_type",
            "item_subtype",
            "pattern",
            "formality",
            "occasions",
        ]
