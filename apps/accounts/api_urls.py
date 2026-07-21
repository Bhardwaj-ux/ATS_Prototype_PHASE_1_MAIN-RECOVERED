from django.urls import path
from .api_views import csrf, login_view, logout_view, me

urlpatterns = [
    path("csrf/", csrf, name="api-csrf"),
    path("login/", login_view, name="api-login"),
    path("logout/", logout_view, name="api-logout"),
    path("me/", me, name="api-me"),
]
