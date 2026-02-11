import pytest
from fastapi import status


class TestVehicleCRUD:
    """Tests para operaciones CRUD de vehículos"""
    
    def test_create_vehicle_as_admin(self, client, admin_headers):
        """Test crear vehículo como admin"""
        vehicle_data = {
            "placa": "ABC-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo",
            "estado": "Activo"
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["placa"] == "ABC-1234"
        assert data["marca"] == "Toyota"
        assert "id" in data
        assert "fechaCreacion" in data
    
    def test_create_vehicle_as_user(self, client, user_headers):
        """Test crear vehículo como usuario normal"""
        vehicle_data = {
            "placa": "XYZ-5678",
            "marca": "Honda",
            "modelo": "Civic",
            "color": "Azul",
            "estado": "Activo"
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=user_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_create_vehicle_without_auth(self, client):
        """Test crear vehículo sin autenticación"""
        vehicle_data = {
            "placa": "ABC-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        response = client.post("/api/vehiculos", json=vehicle_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_vehicle_duplicate_placa(self, client, admin_headers):
        """Test crear vehículo con placa duplicada"""
        vehicle_data = {
            "placa": "DUP-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        # Primer vehículo
        response1 = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Segundo vehículo con misma placa
        response2 = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response2.status_code == status.HTTP_409_CONFLICT
        assert "existe" in response2.json()["detail"].lower()
    
    def test_create_vehicle_invalid_placa_format(self, client, admin_headers):
        """Test crear vehículo con formato de placa inválido"""
        vehicle_data = {
            "placa": "INVALID",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_vehicle_missing_required_fields(self, client, admin_headers):
        """Test crear vehículo sin campos requeridos"""
        vehicle_data = {
            "placa": "ABC-1234"
            # Faltan campos requeridos
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_vehicle_short_modelo(self, client, admin_headers):
        """Test crear vehículo con modelo muy corto"""
        vehicle_data = {
            "placa": "ABC-1234",
            "marca": "Toyota",
            "modelo": "AB",  # Muy corto
            "color": "Rojo"
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_list_vehicles_as_admin(self, client, admin_headers):
        """Test listar vehículos como admin"""
        # Crear algunos vehículos
        for i in range(3):
            vehicle_data = {
                "placa": f"LST-{i}234",
                "marca": "Toyota",
                "modelo": "Corolla",
                "color": "Rojo"
            }
            client.post("/api/vehiculos", json=vehicle_data, headers=admin_headers)
        
        response = client.get("/api/vehiculos", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "vehicles" in data
        assert "total" in data
        assert data["total"] >= 3
    
    def test_list_vehicles_as_user_forbidden(self, client, user_headers):
        """Test listar vehículos como usuario normal (no permitido)"""
        response = client.get("/api/vehiculos", headers=user_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_vehicle_by_id(self, client, admin_headers):
        """Test obtener vehículo por ID"""
        # Crear vehículo
        vehicle_data = {
            "placa": "GET-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        create_response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        vehicle_id = create_response.json()["id"]
        
        # Obtener vehículo
        response = client.get(f"/api/vehiculos/{vehicle_id}", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == vehicle_id
        assert data["placa"] == "GET-1234"
    
    def test_get_vehicle_not_found(self, client, admin_headers):
        """Test obtener vehículo inexistente"""
        response = client.get("/api/vehiculos/99999", headers=admin_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_vehicle_as_admin(self, client, admin_headers):
        """Test actualizar vehículo como admin"""
        # Crear vehículo
        vehicle_data = {
            "placa": "UPD-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        create_response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        vehicle_id = create_response.json()["id"]
        
        # Actualizar vehículo
        update_data = {
            "color": "Azul",
            "estado": "Inactivo"
        }
        response = client.put(
            f"/api/vehiculos/{vehicle_id}",
            json=update_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["color"] == "Azul"
        assert data["estado"] == "Inactivo"
    
    def test_update_vehicle_as_user_forbidden(self, client, user_headers, admin_headers):
        """Test actualizar vehículo como usuario normal (no permitido)"""
        # Crear vehículo como admin
        vehicle_data = {
            "placa": "UPD-5678",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        create_response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        vehicle_id = create_response.json()["id"]
        
        # Intentar actualizar como usuario
        update_data = {"color": "Azul"}
        response = client.put(
            f"/api/vehiculos/{vehicle_id}",
            json=update_data,
            headers=user_headers
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_vehicle_as_admin(self, client, admin_headers):
        """Test eliminar vehículo como admin"""
        # Crear vehículo
        vehicle_data = {
            "placa": "DEL-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        create_response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        vehicle_id = create_response.json()["id"]
        
        # Eliminar vehículo
        response = client.delete(
            f"/api/vehiculos/{vehicle_id}",
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que ya no existe
        get_response = client.get(
            f"/api/vehiculos/{vehicle_id}",
            headers=admin_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_vehicle_as_user_forbidden(self, client, user_headers, admin_headers):
        """Test eliminar vehículo como usuario normal (no permitido)"""
        # Crear vehículo como admin
        vehicle_data = {
            "placa": "DEL-5678",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        create_response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        vehicle_id = create_response.json()["id"]
        
        # Intentar eliminar como usuario
        response = client.delete(
            f"/api/vehiculos/{vehicle_id}",
            headers=user_headers
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestVehicleValidations:
    """Tests para validaciones de vehículos"""
    
    def test_placa_uppercase_conversion(self, client, admin_headers):
        """Test que la placa se convierte a mayúsculas"""
        vehicle_data = {
            "placa": "abc-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo"
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["placa"] == "ABC-1234"
    
    def test_valid_placa_formats(self, client, admin_headers):
        """Test formatos válidos de placa"""
        valid_placas = ["ABC-1234", "XYZ1234", "DEF-567"]
        
        for i, placa in enumerate(valid_placas):
            vehicle_data = {
                "placa": placa,
                "marca": "Toyota",
                "modelo": f"Modelo{i}",
                "color": "Rojo"
            }
            response = client.post(
                "/api/vehiculos",
                json=vehicle_data,
                headers=admin_headers
            )
            assert response.status_code == status.HTTP_201_CREATED
    
    def test_invalid_estado_values(self, client, admin_headers):
        """Test valores inválidos para estado"""
        vehicle_data = {
            "placa": "ABC-1234",
            "marca": "Toyota",
            "modelo": "Corolla",
            "color": "Rojo",
            "estado": "Invalid"
        }
        response = client.post(
            "/api/vehiculos",
            json=vehicle_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
