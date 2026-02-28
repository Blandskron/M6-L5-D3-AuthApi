<!-- Proyecto creado por blandskron -->

# Documentación detallada del proyecto Auth API

## 1. Objetivo

Este repositorio implementa un microservicio de autenticación y perfil con Django + DRF.
Su alcance principal es:

- Registro de usuarios.
- Inicio/cierre de sesión por cookies de sesión.
- Endpoint para obtener usuario autenticado.
- Gestión del perfil asociado al usuario (texto + foto).
- Exposición de contrato OpenAPI con interfaz Swagger/ReDoc.

No está orientado a JWT ni a OAuth; está diseñado para flujo web tradicional con sesión.

## 2. Arquitectura general

El sistema está dividido en tres apps principales dentro de `authproject`:

1. **config**: configuración global Django (settings, rutas raíz, WSGI/ASGI).
2. **authapp**: dominio de autenticación y perfil.
3. **docs**: publicación de schema OpenAPI y UIs de documentación.

Patrón principal usado:

- **Model + Serializer + View (DRF)** para exponer API REST.
- **SessionAuthentication** para seguridad.
- **Router de DRF** para CRUD del perfil.

## 3. Módulos clave

### 3.1 `authapp/models.py`

Define el modelo `Profile` con relación 1:1 hacia `User` de Django.

Responsabilidades:

- Extender datos de usuario sin modificar `auth_user`.
- Persistir biografía, teléfono, fecha de nacimiento y foto.
- Guardar timestamps de creación/actualización.

### 3.2 `authapp/serializers.py`

- `RegisterSerializer`: crea usuario usando `create_user` y crea su perfil inicial.
- `LoginSerializer`: valida username/password para login.
- `UserSerializer`: respuesta mínima de identidad.
- `ProfileSerializer`: serialización completa de perfil con campos de auditoría en solo lectura.

### 3.3 `authapp/views.py`

Contiene dos grupos de endpoints:

1. **Auth (function-based views)**
   - `csrf_token_view`
   - `register_view`
   - `login_view`
   - `logout_view`
   - `me_view`

2. **Profile (ModelViewSet)**
   - `ProfileViewSet`
   - Queryset restringido al usuario autenticado.
   - Parsers de formulario y multipart para soportar foto.
   - Operación de upsert en `create/update/partial_update`.

### 3.4 `authapp/authentication.py`

Incluye `CsrfExemptSessionAuthentication`, pensada solo para desarrollo.
Sobrescribe `enforce_csrf` para evitar errores al probar con Swagger cuando no se maneja encabezado CSRF desde cliente.

### 3.5 `docs/urls.py`

Publica endpoints:

- `/docs/schema/`
- `/docs/swagger/`
- `/docs/redoc/`

## 4. Flujo funcional

### 4.1 Registro

1. Cliente envía `POST /api/register/`.
2. Serializador valida payload.
3. Se crea `User` con hashing de contraseña.
4. Se crea `Profile` asociado automáticamente.
5. Respuesta con datos básicos del usuario.

### 4.2 Login por sesión

1. Cliente solicita `GET /api/csrf/`.
2. Cliente envía `POST /api/login/` con credenciales.
3. Django autentica y registra sesión.
4. Cliente recibe cookie de sesión y puede invocar rutas protegidas.

### 4.3 Perfil

1. Cliente autenticado llama `/api/perfil/*`.
2. El queryset solo devuelve perfil del usuario actual.
3. Si no existe perfil en ciertos flujos, el sistema lo crea.
4. Si se envía archivo `photo`, se guarda en `MEDIA_ROOT/profiles/`.

## 5. Seguridad actual y consideraciones

Fortalezas:

- Uso de autenticación de sesión estándar de Django.
- Permisos `IsAuthenticated` en recursos sensibles.
- Aislamiento por usuario para evitar acceso a perfiles ajenos.

Riesgos/control técnico pendiente:

- Existe bypass de CSRF en `ProfileViewSet` para desarrollo.
- Recomendado para producción:
  - remover `CsrfExemptSessionAuthentication`;
  - activar flujo CSRF completo;
  - configurar `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `CSRF_TRUSTED_ORIGINS`;
  - agregar hardening (CORS/hosts/rate limiting/logging).

## 6. Dependencias

- Django
- djangorestframework
- drf-spectacular
- Pillow

`requirements.txt` define versiones concretas para reproducibilidad.

## 7. Ejecución local recomendada

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python authproject/manage.py migrate
python authproject/manage.py runserver
```

## 8. Posibles mejoras

- Tests unitarios de serializers y vistas.
- Tests de integración para login y perfil multipart.
- Eliminación del bypass CSRF para ambientes productivos.
- Validaciones adicionales de formato de teléfono/imagen.
- Versionado de API (`/api/v1/`).
- Observabilidad (logging estructurado y métricas).

## 9. Convenciones del repositorio

- Endpoints de negocio bajo prefijo `/api/`.
- Documentación OpenAPI bajo `/docs/`.
- Perfil como extensión de `User` vía OneToOne.
- Subida de medios usando `MEDIA_URL` y `MEDIA_ROOT`.
