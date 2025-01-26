from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/vehicles",
    tags=['Vehicles']
)


# @router.get("/", response_model=List[schemas.vehicle])
@router.get("/", response_model=List[schemas.VehicleOut])
def get_vehicles(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    vehicles = db.query(models.Vehicle).filter(models.Vehicle.brand.contains(search)).limit(limit).offset(skip).all()
    return vehicles


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VehicleOut)
def create_vehicles(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


@router.get("/{id}", response_model=schemas.VehicleOut)
def get_vehicle(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vehicle with id: {id} was not found")

    return vehicle


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle_query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = vehicle_query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vehicle with id: {id} does not exist")

    vehicle_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.VehicleOut)
def update_vehicle(id: int, updated_vehicle: schemas.VehicleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle_query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = vehicle_query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vehicle with id: {id} does not exist")

    vehicle_query.update(updated_vehicle.model_dump(), synchronize_session=False)

    db.commit()

    return vehicle_query.first()