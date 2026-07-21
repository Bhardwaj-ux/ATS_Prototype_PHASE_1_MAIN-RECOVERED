from rest_framework import serializers
from .models import User, UserPreference


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "department", "phone"]


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            "profile_name",
            "theme",
            "sidebar_collapsed",
            "compact_tables",
            "email_notifications",
        ]
