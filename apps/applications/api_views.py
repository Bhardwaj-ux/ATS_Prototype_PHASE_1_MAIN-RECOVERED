from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .api_serializers import ApplicationSerializer
from .services import record_status_change


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (
            Application.objects.select_related("job")
            .prefetch_related("status_history")
            .all()
        )
        job_id = self.request.query_params.get("job")
        status = self.request.query_params.get("status")
        if job_id:
            qs = qs.filter(job_id=job_id)
        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        record_status_change(
            instance,
            self.request.user,
            "",
            instance.status,
            "Initial application status",
        )

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        record_status_change(
            instance,
            self.request.user,
            old_status,
            instance.status,
            "Application updated",
        )

    @action(detail=True, methods=["post"], url_path="status/(?P<new_status>[^/.]+)")
    def quick_status(self, request, pk=None, new_status=None):
        application = self.get_object()
        old_status = application.status
        application.status = new_status
        application.save(update_fields=["status", "updated_at"])
        record_status_change(
            application, request.user, old_status, new_status, "Quick action"
        )
        return Response(ApplicationSerializer(application).data)
