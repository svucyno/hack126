"""accounts app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile_view, name="auth-profile"),
    path("profile/update/", views.update_profile_view, name="auth-profile-update"),
    path("logout/", views.logout_view, name="auth-logout"),
    path("status/", views.auth_status_view, name="auth-status"),
]
