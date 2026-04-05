"""outfits app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_outfit_view, name="outfit-generate"),
    path("style-me/", views.style_me_view, name="outfit-style-me"),
    path("looks/", views.saved_looks_list, name="saved-looks-list"),
    path("looks/<int:pk>/", views.saved_look_detail, name="saved-look-detail"),
]
