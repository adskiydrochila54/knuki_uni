"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/', include('uploads.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# === Swagger / OpenAPI ===
swagger_urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += swagger_urlpatterns

# === Static & Media (dev only) ===
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=getattr(settings, 'STATIC_ROOT', None))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
