from rest_framework import serializers
from .models import Application, CandidateStatusHistory


class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = CandidateStatusHistory
        fields = [
            "id",
            "old_status",
            "new_status",
            "note",
            "created_at",
            "changed_by_name",
        ]

    def get_changed_by_name(self, obj):
        return obj.changed_by.full_name if obj.changed_by else None


class ApplicationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)
    skill_list = serializers.SerializerMethodField(read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "job",
            "job_title",
            "full_name",
            "email",
            "phone",
            "current_location",
            "total_experience_years",
            "source",
            "status",
            "status_display",
            "summary",
            "skills",
            "skill_list",
            "status_history",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_skill_list(self, obj):
        return obj.skill_list()

    def validate_skills(self, value):
        parts = (value or "").replace("\n", ",").split(",")
        cleaned, seen = [], set()
        for part in parts:
            s = part.strip()
            if not s or s.lower() in seen:
                continue
            seen.add(s.lower())
            cleaned.append(s)
        return ", ".join(cleaned)
