from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserPreference


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@company.com",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
    )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "phone", "job_title"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Jane Doe"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "you@company.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+91 98765 43210"}
            ),
            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Talent Acquisition Lead",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        if password2:
            validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
