# 🛡 Auth Microservice — Django + DRF

Microservicio de autenticación y gestión de perfil desarrollado con:

* Django
* Django REST Framework
* drf-spectacular (Swagger + ReDoc)
* Autenticación basada en sesión (NO JWT)
* Soporte de subida de imagen en perfil (multipart/form-data)

---

# 📦 Estructura del Proyecto

```
authproject/
│
├── config/              # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│
├── authapp/             # App principal
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── authentication.py
│   ├── urls.py
│
├── docs/                # Swagger / ReDoc
│   ├── urls.py
│
└── manage.py
```

---

# 🚀 Instalación

## 1️⃣ Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

## 2️⃣ Instalar dependencias

```bash
pip install django djangorestframework drf-spectacular pillow
```

---

## 3️⃣ Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4️⃣ Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

---

## 5️⃣ Ejecutar servidor

```bash
python manage.py runserver
```

---

# 📚 Documentación

Swagger:

```
http://127.0.0.1:8000/docs/swagger/
```

ReDoc:

```
http://127.0.0.1:8000/docs/redoc/
```

Schema OpenAPI:

```
http://127.0.0.1:8000/docs/schema/
```

---

# 🔐 Autenticación

Este microservicio usa:

* `SessionAuthentication`
* Cookies de sesión
* CSRF protection (deshabilitado temporalmente solo en Perfil para pruebas Swagger)

Flujo recomendado:

1. `GET /api/csrf/`
2. `POST /api/login/`
3. Usar endpoints protegidos

---

# 📌 Endpoints

## 🧩 Auth

| Método | Endpoint         | Descripción         |
| ------ | ---------------- | ------------------- |
| GET    | `/api/csrf/`     | Obtener CSRF token  |
| POST   | `/api/register/` | Registrar usuario   |
| POST   | `/api/login/`    | Iniciar sesión      |
| POST   | `/api/logout/`   | Cerrar sesión       |
| GET    | `/api/me/`       | Usuario autenticado |

---

## 👤 Profile

Requiere autenticación.

| Método | Endpoint            | Descripción           |
| ------ | ------------------- | --------------------- |
| GET    | `/api/perfil/`      | Listar perfil         |
| GET    | `/api/perfil/{id}/` | Obtener perfil        |
| POST   | `/api/perfil/`      | Crear perfil          |
| PUT    | `/api/perfil/{id}/` | Actualizar perfil     |
| PATCH  | `/api/perfil/{id}/` | Actualización parcial |
| DELETE | `/api/perfil/{id}/` | Eliminar perfil       |

---

# 🖼 Subida de Imagen

El endpoint de perfil acepta:

```
multipart/form-data
```

Campos:

* bio (string)
* phone (string)
* birth_date (date)
* photo (file - binary)

Ejemplo curl:

```bash
curl -X POST http://127.0.0.1:8000/api/perfil/ \
  -H "accept: application/json" \
  -F "bio=Mi biografía" \
  -F "photo=@img.png"
```

---

# 🗂 Modelo Profile

Extiende el modelo User de Django mediante relación OneToOne:

```python
user = OneToOneField(User)
bio = TextField
phone = CharField
photo = ImageField
birth_date = DateField
created_at = DateTimeField
updated_at = DateTimeField
```

---

# ⚙ Configuración Importante (settings.py)

```python
INSTALLED_APPS += [
    'rest_framework',
    'drf_spectacular',
    'authapp',
    'docs',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

# 🧪 CSRF (Modo Desarrollo)

Para pruebas con Swagger, el ProfileViewSet usa:

```python
CsrfExemptSessionAuthentication
```

⚠️ En producción se recomienda:

* Activar CSRF completamente
* Enviar correctamente `X-CSRFToken`
* Mantener protección activa

---

# 🛡 Seguridad

* No usa JWT
* Usa cookies seguras
* Usa permisos `IsAuthenticated`
* Profile limitado al usuario autenticado
* No expone perfiles de terceros

---

# 📌 Tecnologías

* Python 3.10+
* Django 4+
* DRF
* drf-spectacular
* Pillow

---

# 🧠 Próximas mejoras sugeridas

* Activación por email
* Rate limiting
* Verificación de email
* OAuth2
* Dockerización
* PostgreSQL
* Configuración con variables de entorno (.env)

---

# 👨‍💻 Autor

Proyecto desarrollado como microservicio modular de autenticación y perfil.
