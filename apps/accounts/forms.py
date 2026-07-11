from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, UserPreference


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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "department",
            "job_title",
            "location",
            "linkedin_url",
        ]
        widgets = {
            "linkedin_url": forms.URLInput(
                attrs={"placeholder": "https://linkedin.com/in/your-profile"}
            ),
        }


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]
