from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView
from apps.applications.models import Application
from apps.jobs.models import Job
from apps.resumes.models import ResumeFile


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_count"] = Job.objects.filter(is_active=True).count()
        context["application_count"] = Application.objects.count()
        context["resume_count"] = ResumeFile.objects.count()
        context["status_breakdown"] = (
            Application.objects.values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )
        context["latest_applications"] = Application.objects.select_related("job")[:10]
        return context
