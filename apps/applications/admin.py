from django.contrib import admin
from .models import Application, CandidateStatusHistory


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'status', 'source', 'created_at')
    list_filter = ('status', 'job', 'source')
    search_fields = ('full_name', 'email', 'phone', 'job__title')


@admin.register(CandidateStatusHistory)
class CandidateStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'old_status', 'new_status', 'changed_by', 'created_at')
    list_filter = ('new_status',)
    search_fields = ('application__full_name', 'application__email')