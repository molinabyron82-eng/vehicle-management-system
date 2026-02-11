# 🚂 Guía de Despliegue en Railway

Esta guía te ayudará a desplegar el Sistema de Gestión de Vehículos en Railway paso a paso.

## 📋 Pre-requisitos

- Cuenta en [Railway.app](https://railway.app)
- Cuenta en GitHub (opcional, pero recomendado)
- El código del proyecto

## 🚀 Método 1: Despliegue desde GitHub (Recomendado)

### Paso 1: Subir el Código a GitHub

1. Crea un nuevo repositorio en GitHub
2. Descomprime el archivo `vehicle-management-system.zip`
3. Inicializa git y sube el código:

```bash
cd vehicle-management-system
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

### Paso 2: Conectar con Railway

1. Ve a [railway.app](https://railway.app) e inicia sesión
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway para acceder a tu cuenta de GitHub
5. Selecciona el repositorio que acabas de crear

### Paso 3: Agregar Base de Datos PostgreSQL

1. En tu proyecto de Railway, click en "+ New"
2. Selecciona "Database" → "Add PostgreSQL"
3. Railway creará automáticamente la base de datos
4. La variable `DATABASE_URL` se agregará automáticamente

### Paso 4: Configurar Variables de Entorno

En Railway, ve a tu servicio → "Variables" y agrega:

```
SECRET_KEY=tu-clave-secreta-muy-segura-cambiala-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Importante:** Para generar una SECRET_KEY segura, usa:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Paso 5: Desplegar

1. Railway detectará automáticamente que es una app Python
2. Usará el `Procfile` para iniciar la aplicación
3. El despliegue comenzará automáticamente
4. Espera a que el despliegue termine (verás "Success")

### Paso 6: Obtener la URL

1. En Railway, ve a "Settings"
2. En "Networking", click en "Generate Domain"
3. Tu app estará disponible en: `https://tu-app.up.railway.app`

## 🚀 Método 2: Despliegue con Railway CLI

### Instalación de Railway CLI

```bash
# Con npm
npm i -g @railway/cli

# Con Homebrew (macOS)
brew install railway
```

### Pasos para Desplegar

```bash
# 1. Login en Railway
railway login

# 2. Ir al directorio del proyecto
cd vehicle-management-system

# 3. Inicializar proyecto
railway init

# 4. Agregar PostgreSQL
railway add --plugin postgresql

# 5. Configurar variables de entorno
railway variables set SECRET_KEY=tu-clave-secreta
railway variables set ALGORITHM=HS256
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=30

# 6. Desplegar
railway up

# 7. Abrir en el navegador
railway open
```

## 🔧 Configuración Adicional

### Verificar Variables de Entorno

Después del despliegue, verifica que tienes estas variables:

```
DATABASE_URL          (automática desde PostgreSQL)
SECRET_KEY           (configurada manualmente)
ALGORITHM            (configurada manualmente)
ACCESS_TOKEN_EXPIRE_MINUTES (configurada manualmente)
PORT                 (automática de Railway)
```

### Verificar el Despliegue

1. Accede a `https://tu-app.up.railway.app/health`
   - Deberías ver: `{"status": "healthy"}`

2. Accede a `https://tu-app.up.railway.app/`
   - Deberías ver la información del API

3. Accede a `https://tu-app.up.railway.app/docs`
   - Deberías ver la documentación Swagger

## 🧪 Probar el API Desplegado

### 1. Login

```bash
curl -X POST "https://tu-app.up.railway.app/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Crear Vehículo

```bash
# Primero guarda el token
export TOKEN="tu_token_aqui"

curl -X POST "https://tu-app.up.railway.app/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "marca": "Toyota",
    "modelo": "Corolla",
    "color": "Rojo"
  }'
```

### 3. Listar Vehículos

```bash
curl -X GET "https://tu-app.up.railway.app/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN"
```

## 🔍 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Con Railway CLI
railway logs

# O en el dashboard de Railway
# Project → Tu Servicio → Deployments → View Logs
```

### Métricas

En el dashboard de Railway puedes ver:
- CPU usage
- Memory usage
- Network traffic
- Request rate

## 🐛 Solución de Problemas

### Error: "Application failed to start"

1. Verifica los logs en Railway
2. Asegúrate de que todas las dependencias estén en `requirements.txt`
3. Verifica que el `Procfile` esté correctamente configurado

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Error: "Database connection failed"

1. Verifica que PostgreSQL esté agregado al proyecto
2. Verifica que la variable `DATABASE_URL` exista
3. Reinicia el servicio en Railway

### Error: "Module not found"

1. Verifica que todas las dependencias estén en `requirements.txt`
2. Asegúrate de que la estructura de carpetas sea correcta
3. Haz un nuevo deploy:

```bash
railway up --detach
```

### El API responde muy lento

Railway tiene un "cold start" cuando no hay tráfico:
- La primera petición puede tardar 10-15 segundos
- Peticiones subsecuentes serán rápidas
- Considera usar un plan de pago para instancias siempre activas

## 📊 Límites del Plan Gratuito

Railway Plan Gratuito incluye:
- $5 USD de crédito mensual
- ~500 horas de tiempo de ejecución
- 100 GB de ancho de banda
- 512 MB RAM

Si necesitas más recursos, considera actualizar a un plan de pago.

## 🔄 Actualizaciones Continuas

### Con GitHub (Automático)

Si desplegaste desde GitHub, cada push actualizará automáticamente:

```bash
git add .
git commit -m "Update feature X"
git push origin main
# Railway detectará el cambio y desplegará automáticamente
```

### Con Railway CLI (Manual)

```bash
railway up
```

## 🔒 Seguridad en Producción

### 1. Cambiar SECRET_KEY

**Nunca uses la SECRET_KEY por defecto en producción:**

```bash
# Generar nueva clave
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Actualizar en Railway
railway variables set SECRET_KEY=nueva-clave-generada
```

### 2. Configurar CORS Correctamente

Actualiza `app/core/config.py` para permitir solo tu dominio frontend:

```python
ALLOWED_ORIGINS: List[str] = [
    "https://tu-frontend.com",
    "https://www.tu-frontend.com"
]
```

### 3. Usar HTTPS

Railway proporciona HTTPS automáticamente en todos los dominios.

## 🌐 Conectar Frontend

Si tienes un frontend (React, Vue, etc.), actualiza la URL del API:

```javascript
// Antes (desarrollo)
const API_URL = 'http://localhost:8000';

// Después (producción)
const API_URL = 'https://tu-app.up.railway.app';
```

Y asegúrate de que tu dominio esté en ALLOWED_ORIGINS.

## 📱 Acceso desde Postman

1. Importa la colección del API
2. Crea un entorno "Production"
3. Configura la variable `base_url` = `https://tu-app.up.railway.app`
4. Realiza login y guarda el token
5. Usa el token en las demás peticiones

## 🎉 ¡Listo!

Tu API de Gestión de Vehículos está ahora desplegado en Railway y accesible desde internet.

### URLs Importantes

- API: `https://tu-app.up.railway.app`
- Documentación: `https://tu-app.up.railway.app/docs`
- Health Check: `https://tu-app.up.railway.app/health`

### Próximos Pasos

1. Probar todos los endpoints
2. Configurar tu frontend para usar el API
3. Monitorear los logs y el rendimiento
4. Considerar agregar más features

## 📞 Soporte

- [Documentación de Railway](https://docs.railway.app)
- [Comunidad de Railway](https://discord.gg/railway)
- [FastAPI Docs](https://fastapi.tiangolo.com)

---

**¡Tu API está en producción! 🚀**
