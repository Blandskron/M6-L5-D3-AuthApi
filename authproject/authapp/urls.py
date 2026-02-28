# Proyecto creado por blandskron
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ProfileViewSet,
    csrf_token_view,
    login_view,
    logout_view,
    me_view,
    register_view,
)

# Router DRF para exponer operaciones CRUD del perfil autenticado.
router = DefaultRouter()
router.register('perfil', ProfileViewSet, basename='perfil')

urlpatterns = [
    # Endpoints de autenticación basados en sesión/cookie.
    path('csrf/', csrf_token_view),
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('me/', me_view),

    # Endpoints generados automáticamente por el router para ProfileViewSet.
    path('', include(router.urls)),
]
