from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class VehicleBase(BaseModel):
    placa: str = Field(..., min_length=6, max_length=10, description="Placa del vehículo")
    marca: str = Field(..., min_length=2, max_length=50, description="Marca del vehículo")
    modelo: str = Field(..., min_length=3, max_length=50, description="Modelo del vehículo")
    color: str = Field(..., min_length=3, max_length=30, description="Color del vehículo")
    estado: Optional[str] = Field(default="Activo", description="Estado: Activo/Inactivo")

    @field_validator('placa')
    @classmethod
    def validate_placa(cls, v):
        if not v:
            raise ValueError('La placa es obligatoria')
        # Validar formato de placa (ejemplo: ABC-1234 o ABC1234)
        if not re.match(r'^[A-Z]{3}-?\d{3,4}$', v.upper()):
            raise ValueError('Formato de placa inválido. Use formato: ABC-1234 o ABC1234')
        return v.upper()

    @field_validator('marca')
    @classmethod
    def validate_marca(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('La marca es obligatoria y debe tener al menos 2 caracteres')
        return v.strip()

    @field_validator('modelo')
    @classmethod
    def validate_modelo(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('El modelo debe tener al menos 3 caracteres')
        return v.strip()

    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('El color es obligatorio y debe tener al menos 3 caracteres')
        return v.strip()

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v not in ['Activo', 'Inactivo']:
            raise ValueError('El estado debe ser Activo o Inactivo')
        return v


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=6, max_length=10)
    marca: Optional[str] = Field(None, min_length=2, max_length=50)
    modelo: Optional[str] = Field(None, min_length=3, max_length=50)
    color: Optional[str] = Field(None, min_length=3, max_length=30)
    estado: Optional[str] = None

    @field_validator('placa')
    @classmethod
    def validate_placa(cls, v):
        if v and not re.match(r'^[A-Z]{3}-?\d{3,4}$', v.upper()):
            raise ValueError('Formato de placa inválido. Use formato: ABC-1234 o ABC1234')
        return v.upper() if v else v


class VehicleResponse(VehicleBase):
    id: int
    fechaCreacion: datetime

    class Config:
        from_attributes = True


class VehicleListResponse(BaseModel):
    total: int
    vehicles: list[VehicleResponse]
