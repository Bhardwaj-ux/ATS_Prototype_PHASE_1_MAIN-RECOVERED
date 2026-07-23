from django.contrib import admin
from .models import JDImportBatch, JDImportFile


@admin.register(JDImportBatch)
class JDImportBatchAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "status", "file_count", "created_at")
    list_filter = ("status",)


@admin.register(JDImportFile)
class JDImportFileAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "batch",
        "file_type",
        "status",
        "created_job",
        "created_at",
    )
    list_filter = ("status", "file_type")
    search_fields = ("original_filename",)
