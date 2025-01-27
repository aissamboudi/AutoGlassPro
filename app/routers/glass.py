from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/glasses",
    tags=['Glasses']
)

@router.get("/", response_model=List[schemas.GlassOut])
def get_glasses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    glasses = db.query(models.Glass).filter(models.Glass.name.contains(search)).limit(limit).offset(skip).all()
    return glasses


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.GlassOut)
def create_glasses(glass: schemas.GlassCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_glass = models.Glass(**glass.model_dump())
    db.add(new_glass)
    db.commit()
    db.refresh(new_glass)

    return new_glass


@router.get("/{id}", response_model=schemas.GlassOut)
def get_glass(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    glass = db.query(models.Glass).filter(models.Glass.id == id).first()

    if not glass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"glass with id: {id} was not found")

    return glass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_glass(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    glass_query = db.query(models.Glass).filter(models.Glass.id == id)

    glass = glass_query.first()

    if glass == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"glass with id: {id} does not exist")

    glass_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.GlassOut)
def update_glass(id: int, updated_glass: schemas.GlassUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    glass_query = db.query(models.Glass).filter(models.Glass.id == id)

    glass = glass_query.first()

    if glass == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"glass with id: {id} does not exist")

    glass_query.update(updated_glass.model_dump(), synchronize_session=False)

    db.commit()

    return glass_query.first()