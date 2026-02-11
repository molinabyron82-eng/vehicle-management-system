import pytest
from fastapi import status


class TestAuthentication:
    """Tests para endpoints de autenticación"""
    
    def test_login_admin_success(self, client):
        """Test login exitoso con usuario admin"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["role"] == "ADMIN"
        assert data["username"] == "admin"
    
    def test_login_usuario_success(self, client):
        """Test login exitoso con usuario normal"""
        response = client.post(
            "/api/auth/login",
            json={"username": "usuario", "password": "user123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["role"] == "USUARIO"
    
    def test_login_invalid_credentials(self, client):
        """Test login con credenciales inválidas"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrongpassword"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrectos" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login con usuario inexistente"""
        response = client.post(
            "/api/auth/login",
            json={"username": "noexiste", "password": "password"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_missing_fields(self, client):
        """Test login sin campos requeridos"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
