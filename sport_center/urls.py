from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('pages.urls')),
                  path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
                  # Оновлено з namespace
                  path('services/', include('services.urls')),
                  path('news/', include('news.urls')),

                  # Auth views
            ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)