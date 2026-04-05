"""
URL configuration for DripFit backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Google OAuth (allauth)
    path("accounts/", include("allauth.urls")),

    # DripFit API
    path("api/auth/", include("apps.accounts.urls")),
    path("api/wardrobe/", include("apps.wardrobe.urls")),
    path("api/outfit/", include("apps.outfits.urls")),
    path("api/analyser/", include("apps.analyser.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
