from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserPreference


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = [
            "profile_name",
            "theme",
            "sidebar_collapsed",
            "compact_tables",
            "email_notifications",
        ]
