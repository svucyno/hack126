"""wardrobe app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.wardrobe_list, name="wardrobe-list"),
    path("upload/", views.wardrobe_upload, name="wardrobe-upload"),
    path("<int:pk>/", views.wardrobe_item_detail, name="wardrobe-item-detail"),
]
