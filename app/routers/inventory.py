from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/inventory",
    tags=['Inventory']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InventoryOut)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_inventory = models.Inventory(**inventory.model_dump())
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory

@router.put("/{glass_id}", response_model=schemas.InventoryOut)
def update_inventory(glass_id: int, updated_inventory: schemas.InventoryUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    inventory_query = db.query(models.Inventory).filter(models.Inventory.glass_id == glass_id)

    glass = inventory_query.first()

    if glass == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"glass with id: {id} does not exist")

    inventory_query.update(updated_inventory.model_dump(), synchronize_session=False)

    db.commit()

    return inventory_query.first()