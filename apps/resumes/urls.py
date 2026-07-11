from django.urls import path
from .views import ResumeListView, ResumeUploadView, resume_inline_upload

app_name = 'resumes'

urlpatterns = [
    path('', ResumeListView.as_view(), name='list'),
    path('upload/', ResumeUploadView.as_view(), name='upload'),
    path('inline-upload/', resume_inline_upload, name='inline-upload'),
]