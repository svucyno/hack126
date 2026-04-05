"""wardrobe app — WardrobeItem model."""
from django.db import models
from django.contrib.auth.models import User


class WardrobeItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ("top", "Top"),
        ("bottom", "Bottom"),
        ("shoes", "Shoes"),
        ("accessory", "Accessory"),
    ]
    PATTERN_CHOICES = [
        ("solid", "Solid"),
        ("striped", "Striped"),
        ("checked", "Checked"),
        ("printed", "Printed"),
        ("embroidered", "Embroidered"),
        ("graphic", "Graphic"),
    ]
    OCCASION_CHOICES = [
        ("casual", "Casual"),
        ("formal", "Formal"),
        ("party", "Party"),
        ("sport", "Sport"),
        ("ethnic_festive", "Ethnic & Festive"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wardrobe_items"
    )
    image = models.ImageField(upload_to="wardrobe/%Y/%m/")
    cutout_image = models.ImageField(upload_to="wardrobe/cutouts/%Y/%m/", null=True, blank=True, help_text="Transparent PNG cutout via rembg")
    colour_hex = models.CharField(max_length=7, default="#808080", help_text="Dominant colour extracted by ColourThief")
    colour_name = models.CharField(max_length=50, blank=True, default="")
    item_type = models.CharField(max_length=15, choices=ITEM_TYPE_CHOICES, default="top")
    item_subtype = models.CharField(max_length=50, blank=True, default="")
    pattern = models.CharField(max_length=15, choices=PATTERN_CHOICES, default="solid")
    formality = models.PositiveSmallIntegerField(default=3, help_text="1=very casual, 5=very formal")
    occasions = models.JSONField(default=list, help_text="List of applicable occasions")
    is_sample = models.BooleanField(default=False)
    caption = models.TextField(blank=True, default="", help_text="Generated caption / metadata")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} — {self.item_type} ({self.colour_hex})"

    def to_engine_dict(self) -> dict:
        """Convert to the dict format expected by the colour engine."""
        return {
            "id": self.pk,
            "is_sample": self.is_sample,
            "item_type": self.item_type,
            "item_subtype": self.item_subtype,
            "colour_name": self.colour_name or self.colour_hex,
            "colour_hex": self.colour_hex,
            "pattern": self.pattern,
            "formality": self.formality,
            "occasions": self.occasions,
            "image_url": self.image.url if self.image else None,
            "cutout_image_url": self.cutout_image.url if self.cutout_image else None,
        }
