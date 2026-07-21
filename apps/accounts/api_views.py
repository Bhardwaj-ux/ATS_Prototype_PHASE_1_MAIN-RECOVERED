from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserPreference
from .api_serializers import UserSerializer, UserPreferenceSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    # Calling this sets the csrftoken cookie; frontend hits this once on load.
    get_token(request)
    return Response({"detail": "csrf cookie set"})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)
    if user is None:
        return Response({"detail": "Invalid email or password."}, status=400)
    login(request, user)
    return Response(UserSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail": "logged out"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    prefs, _ = UserPreference.objects.get_or_create(user=request.user)
    return Response(
        {
            "user": UserSerializer(request.user).data,
            "preferences": UserPreferenceSerializer(prefs).data,
        }
    )
