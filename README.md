<!-- Proyecto creado por blandskron -->

# Auth Microservice - Django + DRF

Microservicio de autenticación y gestión de perfil desarrollado con Django Rest Framework.

## Resumen

Este proyecto implementa autenticación basada en sesión/cookies (sin JWT), perfil extendido del usuario y documentación automática OpenAPI con Swagger y ReDoc.

## Estructura del proyecto

```text
authproject/
├── authapp/             # Lógica de autenticación y perfil
├── config/              # Configuración global del proyecto Django
├── docs/                # Endpoints para schema, Swagger y ReDoc
├── media/               # Archivos cargados por usuarios (foto de perfil)
└── manage.py
front/
└── index.html           # Cliente de prueba básico
```

## Instalación y ejecución

### 1) Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 2) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3) Migraciones

```bash
python authproject/manage.py makemigrations
python authproject/manage.py migrate
```

### 4) Crear superusuario (opcional)

```bash
python authproject/manage.py createsuperuser
```

### 5) Levantar servidor

```bash
python authproject/manage.py runserver
```

## Documentación de API

- Swagger: `http://127.0.0.1:8000/docs/swagger/`
- ReDoc: `http://127.0.0.1:8000/docs/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/docs/schema/`

## Flujo de autenticación

1. Solicitar token CSRF con `GET /api/csrf/`.
2. Iniciar sesión con `POST /api/login/`.
3. Consumir endpoints protegidos con cookie de sesión.
4. Cerrar sesión con `POST /api/logout/`.

## Endpoints principales

### Auth

| Método | Endpoint         | Descripción         |
| ------ | ---------------- | ------------------- |
| GET    | `/api/csrf/`     | Obtener CSRF token  |
| POST   | `/api/register/` | Registrar usuario   |
| POST   | `/api/login/`    | Iniciar sesión      |
| POST   | `/api/logout/`   | Cerrar sesión       |
| GET    | `/api/me/`       | Usuario autenticado |

### Perfil

| Método | Endpoint            | Descripción           |
| ------ | ------------------- | --------------------- |
| GET    | `/api/perfil/`      | Listar perfil propio  |
| GET    | `/api/perfil/{id}/` | Obtener perfil propio |
| POST   | `/api/perfil/`      | Crear/actualizar      |
| PUT    | `/api/perfil/{id}/` | Actualización total   |
| PATCH  | `/api/perfil/{id}/` | Actualización parcial |
| DELETE | `/api/perfil/{id}/` | Eliminar perfil       |

## Subida de imagen

Los endpoints de perfil aceptan `multipart/form-data` con los campos:

- `bio` (string)
- `phone` (string)
- `birth_date` (date)
- `photo` (archivo binario)

## Seguridad

- Se usa `SessionAuthentication` y permisos `IsAuthenticated`.
- El queryset de perfil está restringido al usuario autenticado.
- No se exponen perfiles de terceros.
- Existe una clase `CsrfExemptSessionAuthentication` solo para desarrollo y pruebas de Swagger.

## Documentación detallada

Para entender arquitectura, módulos, decisiones de diseño y flujos completos revisa:

- `DOCUMENTACION_PROYECTO.md`
