"""analyser app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.analyse_outfit_view, name="analyser"),
]
