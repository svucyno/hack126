"""outfits app — SavedLook model."""
from django.db import models
from django.contrib.auth.models import User


class SavedLook(models.Model):
    OCCASION_CHOICES = [
        ("casual", "Casual"),
        ("formal", "Formal"),
        ("party", "Party"),
        ("sport", "Sport"),
        ("ethnic_festive", "Ethnic & Festive"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_looks")
    # Full outfit data from the engine
    outfit_data = models.JSONField(help_text="Full outfit items, scores, persona from engine")
    # Quick-access fields for filtering/display
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, default="casual")
    persona = models.CharField(max_length=30, blank=True, default="")
    total_score = models.FloatField(default=0.0)
    note = models.TextField(blank=True, default="", help_text="User's personal note")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} — {self.persona} ({self.occasion}) {self.total_score}"
