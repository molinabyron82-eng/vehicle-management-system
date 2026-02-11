from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from typing import List, Optional


class VehicleService:
    
    @staticmethod
    def create_vehicle(db: Session, vehicle_data: VehicleCreate) -> Vehicle:
        try:
            vehicle = Vehicle(**vehicle_data.model_dump())
            db.add(vehicle)
            db.commit()
            db.refresh(vehicle)
            return vehicle
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un vehículo con la placa {vehicle_data.placa}"
            )
    
    @staticmethod
    def get_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        return db.query(Vehicle).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_vehicle_by_id(db: Session, vehicle_id: int) -> Optional[Vehicle]:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo con ID {vehicle_id} no encontrado"
            )
        return vehicle
    
    @staticmethod
    def update_vehicle(db: Session, vehicle_id: int, vehicle_data: VehicleUpdate) -> Vehicle:
        vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
        
        update_data = vehicle_data.model_dump(exclude_unset=True)
        
        try:
            for field, value in update_data.items():
                setattr(vehicle, field, value)
            
            db.commit()
            db.refresh(vehicle)
            return vehicle
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un vehículo con la placa {vehicle_data.placa}"
            )
    
    @staticmethod
    def delete_vehicle(db: Session, vehicle_id: int) -> bool:
        vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
        db.delete(vehicle)
        db.commit()
        return True
    
    @staticmethod
    def count_vehicles(db: Session) -> int:
        return db.query(Vehicle).count()
