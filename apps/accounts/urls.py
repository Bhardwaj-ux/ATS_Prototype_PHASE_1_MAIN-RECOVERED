from django.urls import path
from .views import SettingsView, UserLoginView, UserLogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("settings/", SettingsView.as_view(), name="settings"),
]