from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleListResponse
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/api/vehiculos", tags=["Vehículos"])


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear vehículo",
    description="Crea un nuevo vehículo. Disponible para roles: ADMIN y USUARIO"
)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crear un nuevo vehículo en el sistema.
    
    **Validaciones:**
    - Placa: obligatoria, única, formato ABC-1234 o ABC1234
    - Marca: obligatoria, mínimo 2 caracteres
    - Modelo: obligatorio, mínimo 3 caracteres
    - Color: obligatorio, mínimo 3 caracteres
    - Estado: Activo o Inactivo (por defecto: Activo)
    
    **Permisos:** ADMIN y USUARIO
    """
    return VehicleService.create_vehicle(db, vehicle)


@router.get(
    "",
    response_model=VehicleListResponse,
    summary="Listar vehículos",
    description="Lista todos los vehículos. Solo disponible para rol: ADMIN"
)
async def list_vehicles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("ADMIN"))
):
    """
    Obtener lista de todos los vehículos registrados.
    
    **Parámetros:**
    - skip: número de registros a omitir (paginación)
    - limit: número máximo de registros a devolver
    
    **Permisos:** Solo ADMIN
    """
    vehicles = VehicleService.get_vehicles(db, skip, limit)
    total = VehicleService.count_vehicles(db)
    return VehicleListResponse(total=total, vehicles=vehicles)


@router.get(
    "/{id}",
    response_model=VehicleResponse,
    summary="Obtener vehículo por ID",
    description="Obtiene un vehículo específico. Disponible para roles: ADMIN y USUARIO"
)
async def get_vehicle(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener detalles de un vehículo específico por su ID.
    
    **Permisos:** ADMIN y USUARIO
    """
    return VehicleService.get_vehicle_by_id(db, id)


@router.put(
    "/{id}",
    response_model=VehicleResponse,
    summary="Actualizar vehículo",
    description="Actualiza un vehículo existente. Solo disponible para rol: ADMIN"
)
async def update_vehicle(
    id: int,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("ADMIN"))
):
    """
    Actualizar datos de un vehículo existente.
    
    **Validaciones:**
    - Si se actualiza la placa, debe mantener formato válido
    - No se puede duplicar placa con otro vehículo
    
    **Permisos:** Solo ADMIN
    """
    return VehicleService.update_vehicle(db, id, vehicle)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar vehículo",
    description="Elimina un vehículo del sistema. Solo disponible para rol: ADMIN"
)
async def delete_vehicle(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("ADMIN"))
):
    """
    Eliminar un vehículo del sistema de forma permanente.
    
    **Permisos:** Solo ADMIN
    """
    VehicleService.delete_vehicle(db, id)
    return None
