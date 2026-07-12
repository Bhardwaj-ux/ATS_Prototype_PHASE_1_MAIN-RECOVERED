from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from apps.applications.models import Application

from .forms import (
    AvatarUploadForm,
    EmailAuthenticationForm,
    RegisterForm,
    UserProfileForm,
)
from .models import User, UserPreference


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    template_name = "auth/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("dashboard:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(
            self.request,
            self.object,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        messages.success(
            self.request, "Welcome to Elecbits ATS! Your account has been created."
        )
        return response
