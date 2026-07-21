from django.urls import path
from .views import FolksView

app_name = 'folks'

urlpatterns = [
    path('', FolksView.as_view(), name='index'),
]