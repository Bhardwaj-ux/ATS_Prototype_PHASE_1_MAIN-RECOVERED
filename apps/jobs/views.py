from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import JobForm
from .models import Job


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(is_active=True)


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/form.html'
    success_url = reverse_lazy('jobs:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'jobs/detail.html'
    context_object_name = 'job'


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/form.html'
    success_url = reverse_lazy('jobs:list')


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/confirm_delete.html'
    success_url = reverse_lazy('jobs:list')
    context_object_name = 'job'