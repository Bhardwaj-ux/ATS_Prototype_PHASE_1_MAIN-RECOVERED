from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    employment_type_display = serializers.CharField(
        source="get_employment_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "department",
            "location",
            "employment_type",
            "employment_type_display",
            "experience_min_years",
            "experience_max_years",
            "description",
            "requirements",
            "status",
            "status_display",
            "created_at",
        ]
        read_only_fields = ["created_at"]
