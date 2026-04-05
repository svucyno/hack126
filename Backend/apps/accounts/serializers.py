"""accounts app serializers."""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    wardrobe_item_count = serializers.ReadOnlyField()
    saved_looks_count = serializers.ReadOnlyField()
    can_upload_wardrobe_item = serializers.ReadOnlyField()
    can_upload_more = serializers.ReadOnlyField(source="can_upload_wardrobe_item")
    can_save_look = serializers.ReadOnlyField()
    can_use_analyser = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            "monk_scale",
            "figure_type",
            "tier",
            "wardrobe_item_count",
            "saved_looks_count",
            "can_upload_wardrobe_item",
            "can_upload_more",
            "can_save_look",
            "can_use_analyser",
            "analyser_uses_this_month",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]
