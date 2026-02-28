# Proyecto creado por blandskron
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Perfil extendido asociado 1:1 al usuario nativo de Django.

    Este modelo concentra datos opcionales que no forman parte del modelo
    `User` base (biografía, teléfono, foto y fecha de nacimiento).
    """

    # Relación uno a uno: cada usuario tiene un único perfil.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    # Campos de negocio opcionales del perfil.
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Campos de auditoría básicos.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Representación legible para panel admin y depuración."""
        return f'Profile of {self.user.username}'
