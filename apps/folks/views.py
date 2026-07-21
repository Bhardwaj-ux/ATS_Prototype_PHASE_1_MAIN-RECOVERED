from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class FolksView(LoginRequiredMixin, TemplateView):
    template_name = 'folks/index.html'