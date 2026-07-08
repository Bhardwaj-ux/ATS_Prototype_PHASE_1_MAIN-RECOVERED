from django.db import models
from apps.applications.models import Application
from apps.core.models import TimeStampedModel


def resume_upload_path(instance, filename):
    return f'resumes/job_{instance.application.job_id}/application_{instance.application_id}/{filename}'


class ResumeFile(TimeStampedModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='resume_files')
    file = models.FileField(upload_to=resume_upload_path)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)
    extracted_text = models.TextField(blank=True)

    def __str__(self):
        return self.original_filename