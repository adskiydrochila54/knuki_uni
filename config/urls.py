"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Uploads",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/contacts/", include("contacts.urls")),
    path("api/v1/", include("uploads.urls")),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# === Swagger / OpenAPI ===
swagger_urlpatterns = [
    path('api/v1/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += swagger_urlpatterns

# === Static & Media (dev only) ===
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=getattr(settings, 'STATIC_ROOT', None))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
