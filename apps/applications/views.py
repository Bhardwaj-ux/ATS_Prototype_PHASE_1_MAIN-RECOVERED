from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.jobs.models import Job
from .forms import ApplicationForm
from .models import Application
from .services import record_status_change


class CandidateListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'candidates/list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        qs = Application.objects.select_related('job').all()
        job_id = self.request.GET.get('job')
        status = self.request.GET.get('status')
        if job_id:
            qs = qs.filter(job_id=job_id)
        if status:
            qs = qs.filter(status=status)
        return qs


class CandidateCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'candidates/form.html'
    success_url = reverse_lazy('applications:list')

    def dispatch(self, request, *args, **kwargs):
        if not Job.objects.filter(is_active=True).exists():
            messages.warning(request, 'Create a job first before adding candidates.')
            return redirect('jobs:create')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['job'].queryset = Job.objects.filter(is_active=True).order_by('title')
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        record_status_change(self.object, self.request.user, '', self.object.status, 'Initial application status')
        return response


class CandidateDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'candidates/detail.html'
    context_object_name = 'application'


class CandidateUpdateView(LoginRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'candidates/form.html'
    success_url = reverse_lazy('applications:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['job'].queryset = Job.objects.filter(is_active=True).order_by('title')
        return form

    def form_valid(self, form):
        old_status = self.get_object().status
        response = super().form_valid(form)
        record_status_change(self.object, self.request.user, old_status, self.object.status, 'Application updated')
        return response


class CandidateDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'candidates/confirm_delete.html'
    success_url = reverse_lazy('applications:list')
    context_object_name = 'application'


@login_required
def quick_status_update(request, pk, new_status):
    application = get_object_or_404(Application, pk=pk)
    old_status = application.status
    application.status = new_status
    application.save(update_fields=['status', 'updated_at'])
    record_status_change(application, request.user, old_status, new_status, 'Quick action')
    messages.success(request, 'Candidate status updated successfully.')
    return redirect('applications:detail', pk=pk)