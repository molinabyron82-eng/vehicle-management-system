# Sistema Web de Gestión de Vehículos

API REST desarrollada con FastAPI para la gestión de vehículos con autenticación JWT y control de roles.

## 🚀 Características

- ✅ API REST completa con operaciones CRUD
- ✅ Autenticación y autorización con JWT
- ✅ Control de roles (ADMIN y USUARIO)
- ✅ Validaciones robustas
- ✅ Manejo de errores HTTP apropiados
- ✅ Documentación Swagger/OpenAPI
- ✅ Tests unitarios completos
- ✅ Configuración CORS
- ✅ Listo para desplegar en Railway

## 📋 Requisitos

- Python 3.12+
- PostgreSQL (producción) o SQLite (desarrollo)

## 🛠️ Instalación Local

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd vehicle-management-system
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 🧪 Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app tests/

# Ejecutar tests específicos
pytest tests/test_auth.py
pytest tests/test_vehicles.py

# Ejecutar tests con output detallado
pytest -v
```

## 📚 Documentación API

Una vez iniciada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Autenticación

### Usuarios de Prueba

#### Administrador
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Rol**: `ADMIN`
- **Permisos**: Crear, listar, actualizar, eliminar vehículos

#### Usuario Normal
- **Usuario**: `usuario`
- **Contraseña**: `user123`
- **Rol**: `USUARIO`
- **Permisos**: Solo crear vehículos y ver por ID

### Obtener Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "ADMIN",
  "username": "admin"
}
```

### Usar Token en Requests

```bash
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚗 Endpoints de Vehículos

### Crear Vehículo
```http
POST /api/vehiculos
Authorization: Bearer {token}
Content-Type: application/json

{
  "placa": "ABC-1234",
  "marca": "Toyota",
  "modelo": "Corolla",
  "color": "Rojo",
  "estado": "Activo"
}
```

### Listar Vehículos (Solo ADMIN)
```http
GET /api/vehiculos
Authorization: Bearer {token}
```

### Obtener Vehículo por ID
```http
GET /api/vehiculos/{id}
Authorization: Bearer {token}
```

### Actualizar Vehículo (Solo ADMIN)
```http
PUT /api/vehiculos/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "color": "Azul",
  "estado": "Inactivo"
}
```

### Eliminar Vehículo (Solo ADMIN)
```http
DELETE /api/vehiculos/{id}
Authorization: Bearer {token}
```

## ✅ Validaciones

### Campo: Placa
- ✅ Obligatorio
- ✅ Único en el sistema
- ✅ Formato: ABC-1234 o ABC1234
- ✅ Se convierte automáticamente a mayúsculas
- ❌ Error 409 si ya existe
- ❌ Error 422 si formato inválido

### Campo: Marca
- ✅ Obligatorio
- ✅ Mínimo 2 caracteres
- ✅ Máximo 50 caracteres

### Campo: Modelo
- ✅ Obligatorio
- ✅ Mínimo 3 caracteres
- ✅ Máximo 50 caracteres

### Campo: Color
- ✅ Obligatorio
- ✅ Mínimo 3 caracteres
- ✅ Máximo 30 caracteres

### Campo: Estado
- ✅ Valores permitidos: "Activo" o "Inactivo"
- ✅ Por defecto: "Activo"

## 📊 Códigos de Estado HTTP

| Código | Descripción | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Vehículo creado exitosamente |
| 204 | No Content | Vehículo eliminado exitosamente |
| 400 | Bad Request | Datos inválidos o faltantes |
| 401 | Unauthorized | Token inválido o no proporcionado |
| 403 | Forbidden | Sin permisos para la operación |
| 404 | Not Found | Vehículo no encontrado |
| 409 | Conflict | Placa duplicada |
| 422 | Unprocessable Entity | Error de validación |
| 500 | Internal Server Error | Error del servidor |

## 🎭 Roles y Permisos

### Rol ADMIN
| Operación | Permitido |
|-----------|-----------|
| Crear vehículo | ✅ |
| Listar vehículos | ✅ |
| Ver vehículo por ID | ✅ |
| Actualizar vehículo | ✅ |
| Eliminar vehículo | ✅ |

### Rol USUARIO
| Operación | Permitido |
|-----------|-----------|
| Crear vehículo | ✅ |
| Listar vehículos | ❌ |
| Ver vehículo por ID | ✅ |
| Actualizar vehículo | ❌ |
| Eliminar vehículo | ❌ |

## 🚀 Despliegue en Railway

### Opción 1: Desde GitHub

1. Sube el código a GitHub
2. En Railway:
   - New Project → Deploy from GitHub
   - Selecciona tu repositorio
3. Agrega las variables de entorno:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=tu-clave-secreta-segura
   ```
4. Railway detectará automáticamente Python y usará el `Procfile`

### Opción 2: Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Agregar base de datos PostgreSQL
railway add

# Desplegar
railway up
```

### Variables de Entorno Requeridas en Railway

```env
DATABASE_URL=<proporcionado por Railway PostgreSQL>
SECRET_KEY=<generar una clave segura>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📁 Estructura del Proyecto

```
vehicle-management-system/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Endpoints de autenticación
│   │   └── vehicles.py      # Endpoints de vehículos
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración
│   │   ├── database.py      # Conexión a BD
│   │   └── security.py      # JWT y seguridad
│   ├── models/
│   │   ├── __init__.py
│   │   └── vehicle.py       # Modelo de vehículo
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Schemas de auth
│   │   └── vehicle.py       # Schemas de vehículo
│   ├── services/
│   │   ├── __init__.py
│   │   └── vehicle_service.py
│   ├── __init__.py
│   └── main.py              # Aplicación principal
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Configuración de tests
│   ├── test_auth.py         # Tests de autenticación
│   └── test_vehicles.py     # Tests de vehículos
├── .env.example
├── .gitignore
├── Procfile
├── README.md
├── railway.json
├── requirements.txt
└── runtime.txt
```

## 🔧 Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos
- **PyJWT**: Implementación de JWT
- **Passlib**: Hashing de contraseñas
- **Pytest**: Framework de testing
- **Uvicorn**: Servidor ASGI

## 📝 Ejemplos de Uso

### Ejemplo 1: Flujo completo con ADMIN

```bash
# 1. Login
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.access_token')

# 2. Crear vehículo
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "XYZ-9876",
    "marca": "Honda",
    "modelo": "Civic",
    "color": "Negro",
    "estado": "Activo"
  }'

# 3. Listar vehículos
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN"

# 4. Actualizar vehículo
curl -X PUT "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"color": "Blanco"}'

# 5. Eliminar vehículo
curl -X DELETE "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Ejemplo 2: Usuario normal

```bash
# Login como usuario
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "user123"}' | jq -r '.access_token')

# Crear vehículo (permitido)
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "USR-1111",
    "marca": "Nissan",
    "modelo": "Sentra",
    "color": "Gris"
  }'

# Intentar listar (denegado)
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN"
# Respuesta: 403 Forbidden
```

## 🐛 Solución de Problemas

### Error: "Token inválido o expirado"
- Verifica que el token esté correctamente copiado
- El token expira en 30 minutos, genera uno nuevo

### Error: "No tiene permisos para realizar esta acción"
- Verifica que tu usuario tenga el rol adecuado
- Algunas operaciones solo están disponibles para ADMIN

### Error: "Ya existe un vehículo con la placa"
- Las placas deben ser únicas
- Usa una placa diferente o actualiza el vehículo existente

### Tests fallan
- Asegúrate de estar en el entorno virtual
- Verifica que todas las dependencias estén instaladas
- Elimina el archivo `test.db` si existe

## 📄 Licencia

Este proyecto fue desarrollado como parte de un sistema académico de gestión de vehículos.

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para problemas o preguntas, abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando FastAPI y Python 3.12**
