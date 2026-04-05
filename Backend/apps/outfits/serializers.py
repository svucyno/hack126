"""outfits app serializers."""
from rest_framework import serializers
from .models import SavedLook


class SavedLookSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedLook
        fields = [
            "id",
            "outfit_data",
            "occasion",
            "persona",
            "total_score",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "persona", "total_score", "created_at"]


class SaveLookCreateSerializer(serializers.ModelSerializer):
    """Serializer for saving a generated look."""
    class Meta:
        model = SavedLook
        fields = ["outfit_data", "occasion", "note"]
