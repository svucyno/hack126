"""accounts app views."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .serializers import UserSerializer
from .models import UserProfile


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Return the authenticated user's profile and tier information."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Update monk_scale and figure_type preferences."""
    profile = request.user.profile
    allowed_fields = {"monk_scale", "figure_type"}
    data = {k: v for k, v in request.data.items() if k in allowed_fields}

    if "monk_scale" in data:
        try:
            val = int(data["monk_scale"])
            if not 1 <= val <= 7:
                return Response({"error": "monk_scale must be 1–7."}, status=400)
            profile.monk_scale = val
        except (ValueError, TypeError):
            return Response({"error": "monk_scale must be an integer."}, status=400)

    if "figure_type" in data:
        if data["figure_type"] not in ["female", "male", "neutral"]:
            return Response({"error": "figure_type must be female, male, or neutral."}, status=400)
        if data["figure_type"] != "female" and profile.tier == "free":
            return Response(
                {"error": "Non-female figure types require a Premium subscription."},
                status=403,
            )
        profile.figure_type = data["figure_type"]

    profile.save()
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Log out the current user."""
    logout(request)
    return Response({"message": "Logged out successfully."})


@api_view(["GET"])
@permission_classes([AllowAny])
def auth_status_view(request):
    """Return auth status without requiring login — used by frontend to check session."""
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response({"authenticated": True, "user": serializer.data})
    return Response({"authenticated": False})
