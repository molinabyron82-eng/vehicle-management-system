# Ejemplos de Uso del API

Este documento contiene ejemplos prácticos de cómo usar el API de Gestión de Vehículos.

## 🔐 Autenticación

### Login como Administrador

**Request:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJBRE1JTiIsImV4cCI6MTcwOTI0MzQwMH0.xxx",
  "token_type": "bearer",
  "role": "ADMIN",
  "username": "admin"
}
```

### Login como Usuario

**Request:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "user123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3VhcmlvIiwicm9sZSI6IlVTVUFSSU8iLCJleHAiOjE3MDkyNDM0MDB9.xxx",
  "token_type": "bearer",
  "role": "USUARIO",
  "username": "usuario"
}
```

## 🚗 Gestión de Vehículos

### 1. Crear Vehículo

**Request (ADMIN o USUARIO):**
```bash
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "marca": "Toyota",
    "modelo": "Corolla 2023",
    "color": "Rojo",
    "estado": "Activo"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "marca": "Toyota",
  "modelo": "Corolla 2023",
  "color": "Rojo",
  "estado": "Activo",
  "fechaCreacion": "2024-02-10T10:30:00"
}
```

### 2. Listar Todos los Vehículos

**Request (Solo ADMIN):**
```bash
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Response (200 OK):**
```json
{
  "total": 3,
  "vehicles": [
    {
      "id": 1,
      "placa": "ABC-1234",
      "marca": "Toyota",
      "modelo": "Corolla 2023",
      "color": "Rojo",
      "estado": "Activo",
      "fechaCreacion": "2024-02-10T10:30:00"
    },
    {
      "id": 2,
      "placa": "XYZ-5678",
      "marca": "Honda",
      "modelo": "Civic 2024",
      "color": "Azul",
      "estado": "Activo",
      "fechaCreacion": "2024-02-10T11:00:00"
    }
  ]
}
```

### 3. Obtener Vehículo por ID

**Request (ADMIN o USUARIO):**
```bash
curl -X GET "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "marca": "Toyota",
  "modelo": "Corolla 2023",
  "color": "Rojo",
  "estado": "Activo",
  "fechaCreacion": "2024-02-10T10:30:00"
}
```

### 4. Actualizar Vehículo

**Request (Solo ADMIN):**
```bash
curl -X PUT "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "color": "Blanco",
    "estado": "Inactivo"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "marca": "Toyota",
  "modelo": "Corolla 2023",
  "color": "Blanco",
  "estado": "Inactivo",
  "fechaCreacion": "2024-02-10T10:30:00"
}
```

### 5. Eliminar Vehículo

**Request (Solo ADMIN):**
```bash
curl -X DELETE "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Response (204 No Content):**
```
(Sin contenido)
```

## ❌ Ejemplos de Errores

### Error 400 - Datos Inválidos

**Request:**
```bash
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "INVALID",
    "marca": "T",
    "modelo": "AB"
  }'
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "placa"],
      "msg": "Formato de placa inválido. Use formato: ABC-1234 o ABC1234"
    },
    {
      "type": "value_error",
      "loc": ["body", "marca"],
      "msg": "La marca es obligatoria y debe tener al menos 2 caracteres"
    },
    {
      "type": "value_error",
      "loc": ["body", "modelo"],
      "msg": "El modelo debe tener al menos 3 caracteres"
    }
  ]
}
```

### Error 401 - No Autenticado

**Request:**
```bash
curl -X GET "http://localhost:8000/api/vehiculos"
```

**Response (403 Forbidden):**
```json
{
  "detail": "Not authenticated"
}
```

### Error 403 - Sin Permisos

**Request (Usuario intentando listar):**
```bash
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer USER_TOKEN"
```

**Response (403 Forbidden):**
```json
{
  "detail": "No tiene permisos para realizar esta acción"
}
```

### Error 404 - No Encontrado

**Request:**
```bash
curl -X GET "http://localhost:8000/api/vehiculos/99999" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (404 Not Found):**
```json
{
  "detail": "Vehículo con ID 99999 no encontrado"
}
```

### Error 409 - Placa Duplicada

**Request:**
```bash
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "marca": "Honda",
    "modelo": "Civic",
    "color": "Negro"
  }'
```

**Response (409 Conflict):**
```json
{
  "detail": "Ya existe un vehículo con la placa ABC-1234"
}
```

## 🔄 Flujos Completos

### Flujo 1: Administrador Completo

```bash
# 1. Login
export TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.access_token')

# 2. Crear varios vehículos
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "AAA-1111",
    "marca": "Toyota",
    "modelo": "Corolla",
    "color": "Rojo"
  }'

curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "BBB-2222",
    "marca": "Honda",
    "modelo": "Civic",
    "color": "Azul"
  }'

# 3. Listar todos
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Actualizar uno
curl -X PUT "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"color": "Verde"}' | jq

# 5. Eliminar uno
curl -X DELETE "http://localhost:8000/api/vehiculos/2" \
  -H "Authorization: Bearer $TOKEN"
```

### Flujo 2: Usuario Normal

```bash
# 1. Login
export USER_TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "user123"}' | jq -r '.access_token')

# 2. Crear vehículo (permitido)
curl -X POST "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "USR-9999",
    "marca": "Nissan",
    "modelo": "Sentra",
    "color": "Gris"
  }' | jq

# 3. Ver vehículo creado (permitido)
curl -X GET "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer $USER_TOKEN" | jq

# 4. Intentar listar todos (denegado)
curl -X GET "http://localhost:8000/api/vehiculos" \
  -H "Authorization: Bearer $USER_TOKEN"
# Respuesta: 403 Forbidden

# 5. Intentar actualizar (denegado)
curl -X PUT "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"color": "Negro"}'
# Respuesta: 403 Forbidden

# 6. Intentar eliminar (denegado)
curl -X DELETE "http://localhost:8000/api/vehiculos/1" \
  -H "Authorization: Bearer $USER_TOKEN"
# Respuesta: 403 Forbidden
```

## 🧪 Pruebas con Python

### Script de Prueba Completo

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Login
def login(username, password):
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": username, "password": password}
    )
    return response.json()["access_token"]

# Crear vehículo
def create_vehicle(token, vehicle_data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/vehiculos",
        json=vehicle_data,
        headers=headers
    )
    return response.json()

# Uso
admin_token = login("admin", "admin123")

vehicle = create_vehicle(admin_token, {
    "placa": "PY-12345",
    "marca": "Toyota",
    "modelo": "Yaris",
    "color": "Blanco"
})

print(f"Vehículo creado: {vehicle}")
```

## 📱 Integración Frontend (JavaScript)

```javascript
const API_URL = 'http://localhost:8000';

// Login
async function login(username, password) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  localStorage.setItem('role', data.role);
  return data;
}

// Crear vehículo
async function createVehicle(vehicleData) {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_URL}/api/vehiculos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(vehicleData)
  });
  
  return await response.json();
}

// Listar vehículos (solo admin)
async function listVehicles() {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_URL}/api/vehiculos`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  return await response.json();
}

// Uso
async function main() {
  // Login
  await login('admin', 'admin123');
  
  // Crear vehículo
  const vehicle = await createVehicle({
    placa: 'JS-98765',
    marca: 'Honda',
    modelo: 'Accord',
    color: 'Negro'
  });
  
  console.log('Vehículo creado:', vehicle);
  
  // Listar
  const list = await listVehicles();
  console.log('Vehículos:', list);
}

main();
```

---

Para más información, consulta el [README.md](README.md) principal.
