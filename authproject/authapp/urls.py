from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_view,
    login_view,
    logout_view,
    csrf_token_view,
    me_view,
    ProfileViewSet
)

router = DefaultRouter()
router.register('perfil', ProfileViewSet, basename='perfil')

urlpatterns = [
    path('csrf/', csrf_token_view),
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('me/', me_view),
    path('', include(router.urls)),
]