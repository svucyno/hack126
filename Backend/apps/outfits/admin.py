"""outfits app admin."""
from django.contrib import admin
from .models import SavedLook


@admin.register(SavedLook)
class SavedLookAdmin(admin.ModelAdmin):
    list_display = ["user", "persona", "occasion", "total_score", "created_at"]
    list_filter = ["occasion", "persona"]
    search_fields = ["user__email"]
    readonly_fields = ["created_at"]
