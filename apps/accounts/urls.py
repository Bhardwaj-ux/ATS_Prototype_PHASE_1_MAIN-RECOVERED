from django.urls import path
from .views import UserLoginView, UserLogoutView, settings_view, upload_avatar

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("settings/", settings_view, name="settings"),
    path("settings/avatar/", upload_avatar, name="upload-avatar"),
]
