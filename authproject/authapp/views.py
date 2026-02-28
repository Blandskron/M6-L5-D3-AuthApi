# Proyecto creado por blandskron
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import parsers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .authentication import CsrfExemptSessionAuthentication
from .models import Profile
from .serializers import (
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)


@extend_schema(
    tags=["Auth"],
    summary="Obtener CSRF token",
    description="Devuelve un CSRF token para autenticación basada en sesión/cookies.",
    responses={200: OpenApiResponse(description="CSRF token retornado")},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    """Retorna token CSRF para clientes que trabajan con sesión/cookie."""
    return Response({'csrfToken': get_token(request)})


@extend_schema(
    tags=["Auth"],
    summary="Registro de usuario",
    description="Crea un usuario (User Django) y crea automáticamente su Profile.",
    request=RegisterSerializer,
    responses={201: UserSerializer},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Registra un usuario nuevo y responde con los datos públicos del usuario."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Auth"],
    summary="Login",
    description="Autentica por username/password y crea sesión (cookie). No usa JWT.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="Login exitoso"),
        400: OpenApiResponse(description="Credenciales inválidas"),
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Inicia sesión persistiendo cookie de sesión en la respuesta."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
    )

    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=400)

    login(request, user)
    return Response({'detail': 'Logged in successfully'})


@extend_schema(
    tags=["Auth"],
    summary="Logout",
    description="Cierra la sesión actual. Requiere autenticación.",
    responses={200: OpenApiResponse(description="Logout exitoso")},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Finaliza sesión del usuario autenticado."""
    logout(request)
    return Response({'detail': 'Logged out successfully'})


@extend_schema(
    tags=["Auth"],
    summary="Me",
    description="Devuelve el usuario autenticado.",
    responses={200: UserSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Retorna identidad del usuario de la sesión activa."""
    return Response(UserSerializer(request.user).data)


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema_view(
    create=extend_schema(
        tags=["Profile"],
        summary="Crear mi perfil",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "bio": {"type": "string"},
                    "phone": {"type": "string"},
                    "birth_date": {"type": "string", "format": "date"},
                    "photo": {"type": "string", "format": "binary"},
                },
                "required": [],
            },
        },
        responses={201: ProfileSerializer},
    ),
    update=extend_schema(
        tags=["Profile"],
        summary="Actualizar mi perfil (PUT)",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "bio": {"type": "string"},
                    "phone": {"type": "string"},
                    "birth_date": {"type": "string", "format": "date"},
                    "photo": {"type": "string", "format": "binary"},
                },
                "required": [],
            },
        },
        responses={200: ProfileSerializer},
    ),
    partial_update=extend_schema(
        tags=["Profile"],
        summary="Actualizar mi perfil (PATCH)",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "bio": {"type": "string"},
                    "phone": {"type": "string"},
                    "birth_date": {"type": "string", "format": "date"},
                    "photo": {"type": "string", "format": "binary"},
                },
                "required": [],
            },
        },
        responses={200: ProfileSerializer},
    ),
    destroy=extend_schema(
        tags=["Profile"],
        summary="Eliminar mi perfil",
        responses={204: OpenApiResponse(description="Eliminado")},
    ),
)
class ProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD del perfil del usuario autenticado.

    - Restringe el queryset al usuario en sesión para evitar acceso cruzado.
    - Acepta multipart/form-data para permitir carga de imagen de perfil.
    - Usa autenticación de sesión sin CSRF únicamente para facilitar pruebas.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get_queryset(self):
        """Aísla el acceso al perfil del usuario autenticado actual."""
        return Profile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Mantiene ProfileSerializer como serializador de este viewset."""
        return ProfileSerializer

    def create(self, request, *args, **kwargs):
        """Crea o actualiza el perfil propio (upsert explícito en create)."""
        photo = request.FILES.get("photo")
        profile, created = Profile.objects.get_or_create(user=request.user)

        bio = request.data.get("bio")
        phone = request.data.get("phone")
        birth_date = request.data.get("birth_date")

        if bio is not None:
            profile.bio = bio
        if phone is not None:
            profile.phone = phone
        if birth_date is not None and str(birth_date).strip():
            profile.birth_date = birth_date
        if photo is not None:
            profile.photo = photo

        profile.save()
        return Response(
            ProfileSerializer(profile).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        """PUT completo soportado como upsert sobre perfil propio."""
        return self._upsert(request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        """PATCH parcial soportado como upsert sobre perfil propio."""
        return self._upsert(request, partial=True)

    def _upsert(self, request, partial: bool):
        """Lógica compartida para crear/actualizar perfil sin exponer otros usuarios."""
        profile = self.get_queryset().first()
        if profile is None:
            profile = Profile.objects.create(user=request.user)

        photo = request.FILES.get("photo")

        if "bio" in request.data:
            profile.bio = request.data.get("bio", "") if request.data.get("bio") is not None else ""
        if "phone" in request.data:
            profile.phone = request.data.get("phone", "") if request.data.get("phone") is not None else ""
        if "birth_date" in request.data:
            bd = request.data.get("birth_date")
            profile.birth_date = None if (bd is None or not str(bd).strip()) else bd
        if photo is not None:
            profile.photo = photo

        profile.save()
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
