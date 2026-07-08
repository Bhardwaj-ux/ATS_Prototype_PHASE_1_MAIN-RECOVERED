from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import ResumeUploadForm
from .models import ResumeFile


class ResumeUploadView(LoginRequiredMixin, CreateView):
    model = ResumeFile
    form_class = ResumeUploadForm
    template_name = 'resumes/upload.html'
    success_url = reverse_lazy('applications:list')

    def form_valid(self, form):
        uploaded = self.request.FILES['file']
        form.instance.original_filename = uploaded.name
        form.instance.file_size = uploaded.size
        form.instance.mime_type = getattr(uploaded, 'content_type', '') or ''
        return super().form_valid(form)


class ResumeListView(LoginRequiredMixin, ListView):
    model = ResumeFile
    template_name = 'resumes/list.html'
    context_object_name = 'resume_files'

    def get_queryset(self):
        return ResumeFile.objects.select_related('application', 'application__job').all()