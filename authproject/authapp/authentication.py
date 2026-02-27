from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SOLO para desarrollo / Swagger.
    Desactiva la validación CSRF en endpoints específicos.
    """
    def enforce_csrf(self, request):
        return  # no-op