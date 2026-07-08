from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import EmailAuthenticationForm, UserPreferenceForm
from .models import UserPreference


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass


class SettingsView(LoginRequiredMixin, UpdateView):
    model = UserPreference
    form_class = UserPreferenceForm
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("accounts:settings")

    def get_object(self, queryset=None):
        obj, created = UserPreference.objects.get_or_create(user=self.request.user)
        if created and not obj.profile_name:
            full_name = self.request.user.get_full_name().strip()
            obj.profile_name = full_name or self.request.user.username
            obj.save(update_fields=["profile_name"])
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Settings updated successfully.")
        return super().form_valid(form)
