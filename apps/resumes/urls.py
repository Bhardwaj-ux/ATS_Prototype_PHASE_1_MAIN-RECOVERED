from django.urls import path
from .views import ResumeListView, ResumeUploadView

app_name = 'resumes'

urlpatterns = [
    path('', ResumeListView.as_view(), name='list'),
    path('upload/', ResumeUploadView.as_view(), name='upload'),
]