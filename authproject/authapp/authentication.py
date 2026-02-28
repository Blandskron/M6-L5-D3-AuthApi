# Proyecto creado por blandskron
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Autenticación de sesión sin validación CSRF.

    Uso previsto: entornos de desarrollo y pruebas desde Swagger UI.
    No debe emplearse en producción porque reduce la protección ante CSRF.
    """

    def enforce_csrf(self, request):
        """Sobrescribe la verificación CSRF para convertirla en no-op."""
        return
