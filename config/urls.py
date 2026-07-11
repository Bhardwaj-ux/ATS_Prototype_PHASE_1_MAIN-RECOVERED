from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='dashboard:index', permanent=False)),
    path('account/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('candidates/', include('apps.applications.urls')),
    path('resumes/', include('apps.resumes.urls')),
    path('folks/', include('apps.folks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)