from django.urls import path
from .views import UserLoginView, UserLogoutView, settings_view

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("settings/", settings_view, name="settings"),
]
