"""accounts app — UserProfile model."""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    TIER_CHOICES = [("free", "Free"), ("premium", "Premium")]
    FIGURE_CHOICES = [("female", "Female"), ("male", "Male"), ("neutral", "Gender-Neutral")]
    MONK_CHOICES = [(i, str(i)) for i in range(1, 8)]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    monk_scale = models.IntegerField(choices=MONK_CHOICES, default=3)
    figure_type = models.CharField(max_length=10, choices=FIGURE_CHOICES, default="female")
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="free")
    analyser_uses_this_month = models.PositiveIntegerField(default=0)
    analyser_reset_month = models.PositiveIntegerField(default=0)  # month number
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} ({self.tier})"

    @property
    def wardrobe_item_count(self):
        return self.user.wardrobe_items.filter(is_sample=False).count()

    @property
    def saved_looks_count(self):
        return self.user.saved_looks.count()

    @property
    def can_upload_wardrobe_item(self):
        if self.tier == "premium":
            return True
        return self.wardrobe_item_count < 10  # free tier max

    @property
    def can_save_look(self):
        if self.tier == "premium":
            return True
        return self.saved_looks_count < 3  # free tier max

    @property
    def can_use_analyser(self):
        if self.tier == "premium":
            return True
        from django.utils import timezone
        current_month = timezone.now().month
        if self.analyser_reset_month != current_month:
            return True  # will reset on use
        return self.analyser_uses_this_month < 3  # free: 3/month

    def increment_analyser_uses(self):
        from django.utils import timezone
        current_month = timezone.now().month
        if self.analyser_reset_month != current_month:
            self.analyser_uses_this_month = 1
            self.analyser_reset_month = current_month
        else:
            self.analyser_uses_this_month += 1
        self.save(update_fields=["analyser_uses_this_month", "analyser_reset_month"])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
