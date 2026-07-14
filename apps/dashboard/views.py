from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from apps.applications.models import Application, CandidateStatusHistory
from apps.jobs.models import Job
from apps.resumes.models import ResumeFile
from apps.tasks.models import Task

ACTIVITY_VERB_MAP = {
    "hired": "hired",
    "rejected": "rejected",
    "shortlisted": "shortlisted",
    "interview": "moved to interview",
    "under_review": "marked under review",
}


def build_recent_activity():
    rows = (
        CandidateStatusHistory.objects.filter(
            changed_by__isnull=False, new_status__in=ACTIVITY_VERB_MAP.keys()
        )
        .values("changed_by__full_name", "changed_by__email", "new_status")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    activity = []
    for row in rows:
        name = row["changed_by__full_name"] or row["changed_by__email"]
        verb = ACTIVITY_VERB_MAP.get(row["new_status"], row["new_status"])
        count = row["total"]
        noun = "candidate" if count == 1 else "candidates"
        activity.append(f"{name} {verb} {count} {noun}")
    return activity


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_count"] = Job.objects.filter(is_active=True).count()
        context["interview_count"] = Application.objects.filter(
            status="interview"
        ).count()
        context["candidates_hired"] = Application.objects.filter(status="hired").count()
        context["open_positions"] = Job.objects.filter(is_active=True).count()
        context["candidate_count"] = Application.objects.count()
        context["shortlisted_count"] = Application.objects.filter(status="shortlisted").count()
        context["status_breakdown"] = (
            Application.objects.values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )
        context["latest_applications"] = Application.objects.select_related("job")[:10]
        context["tasks"] = Task.objects.filter(owner=self.request.user)
        context["recent_activity"] = build_recent_activity()
        return context
