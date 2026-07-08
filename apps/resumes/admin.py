from django.contrib import admin
from .models import ResumeFile


@admin.register(ResumeFile)
class ResumeFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'application', 'file_size', 'created_at')
    search_fields = ('original_filename', 'application__full_name', 'application__email')