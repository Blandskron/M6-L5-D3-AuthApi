# Proyecto creado por blandskron
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para registrar usuarios y crear su perfil inicial."""

    # La contraseña solo debe entrar por escritura; nunca se devuelve.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        """Crea el usuario usando el helper seguro de Django y su Profile."""
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Valida credenciales para iniciar sesión por cookie/sesión."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Expone datos mínimos del usuario autenticado."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    """Serializa el perfil completo con campos de solo lectura controlados."""

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
