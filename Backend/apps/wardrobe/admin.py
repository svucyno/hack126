"""wardrobe app admin."""
from django.contrib import admin
from .models import WardrobeItem


@admin.register(WardrobeItem)
class WardrobeItemAdmin(admin.ModelAdmin):
    list_display = ["user", "item_type", "item_subtype", "colour_hex", "pattern", "formality", "is_sample", "created_at"]
    list_filter = ["item_type", "pattern", "is_sample"]
    search_fields = ["user__email", "colour_name", "item_subtype"]
    readonly_fields = ["colour_hex", "caption", "created_at", "updated_at"]
