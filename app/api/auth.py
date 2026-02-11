from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Base de datos de usuarios en memoria (para demostración)
# En producción, esto debería estar en una base de datos real
# Los hashes se generan cuando se necesitan para evitar problemas en tiempo de importación
def get_users_db():
    """Retorna la base de datos de usuarios con contraseñas hasheadas"""
    return {
        "admin": {
            "username": "admin",
            "password": get_password_hash("admin123"),
            "role": "ADMIN"
        },
        "usuario": {
            "username": "usuario",
            "password": get_password_hash("user123"),
            "role": "USUARIO"
        }
    }


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
async def login(credentials: LoginRequest):
    """
    Endpoint para autenticación de usuarios.
    
    Usuarios de prueba:
    - admin / admin123 (rol ADMIN)
    - usuario / user123 (rol USUARIO)
    """
    USERS_DB = get_users_db()
    user = USERS_DB.get(credentials.username)
    
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=user["role"],
        username=user["username"]
    )
