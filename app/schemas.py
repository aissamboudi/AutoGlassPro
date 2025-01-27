from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class VehicleCreate(BaseModel):
    brand: str
    model: str
    year: int

class VehicleOut(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    created_at: datetime

    class Config:
        from_attributes = True

class GlassCreate(BaseModel):
    name: str
    vehicle_id: int

class GlassOut(BaseModel):
    id: int
    name: str
    vehicle_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class InventoryCreate(BaseModel):
    quantity: int
    price: float
    received_date: datetime
    glass_id: int

class InventoryOut(BaseModel):
    id: int
    quantity: int
    price: int
    received_date: datetime
    created_at: datetime
    glass_id: int
    owner : GlassOut

    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    quantity: int