# Proyecto creado por blandskron
"""Ruteo principal del proyecto Django."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Panel de administración nativo Django.
    path('admin/', admin.site.urls),

    # API principal de autenticación/perfil.
    path('api/', include('authapp.urls')),

    # Endpoints de documentación OpenAPI + UIs.
    path('docs/', include('docs.urls')),
]

# Sirve medios en desarrollo (no recomendado para producción).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
