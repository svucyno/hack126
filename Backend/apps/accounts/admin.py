"""accounts app admin."""
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "tier", "monk_scale", "figure_type", "wardrobe_item_count", "saved_looks_count"]
    list_filter = ["tier", "figure_type"]
    search_fields = ["user__email", "user__first_name"]
    readonly_fields = ["wardrobe_item_count", "saved_looks_count", "created_at"]
