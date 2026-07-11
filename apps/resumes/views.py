from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView

from apps.applications.models import Application
from .forms import ResumeUploadForm
from .models import ResumeFile


class ResumeUploadView(LoginRequiredMixin, CreateView):
    model = ResumeFile
    form_class = ResumeUploadForm
    template_name = "resumes/upload.html"
    success_url = reverse_lazy("applications:list")

    def form_valid(self, form):
        uploaded = self.request.FILES["file"]
        form.instance.original_filename = uploaded.name
        form.instance.file_size = uploaded.size
        form.instance.mime_type = getattr(uploaded, "content_type", "") or ""
        return super().form_valid(form)


class ResumeListView(LoginRequiredMixin, ListView):
    model = ResumeFile
    template_name = "resumes/list.html"
    context_object_name = "resume_files"

    def get_queryset(self):
        return ResumeFile.objects.select_related(
            "application", "application__job"
        ).all()


@login_required
@require_POST
def resume_inline_upload(request):
    application_id = request.POST.get("application_id")
    application = get_object_or_404(Application, pk=application_id)

    uploaded = request.FILES.get("file")
    if not uploaded:
        return JsonResponse({"ok": False, "error": "No file was received."}, status=400)

    form = ResumeUploadForm(
        data={"application": application.pk},
        files={"file": uploaded},
    )
    if not form.is_valid():
        error_list = (
            form.errors.get("file") or form.errors.get("__all__") or ["Upload failed."]
        )
        return JsonResponse({"ok": False, "error": " ".join(error_list)}, status=400)

    resume = form.save(commit=False)
    resume.original_filename = uploaded.name
    resume.file_size = uploaded.size
    resume.mime_type = getattr(uploaded, "content_type", "") or ""
    resume.save()

    return JsonResponse(
        {
            "ok": True,
            "file": {
                "id": resume.pk,
                "name": resume.original_filename,
                "url": resume.file.url,
                "size": resume.file_size,
            },
        }
    )
