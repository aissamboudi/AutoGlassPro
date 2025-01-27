from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
class Glass(Base):
    __tablename__ = 'glasses'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    vehicle_id = Column(Integer, ForeignKey(
        "vehicles.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Vehicle")

class Inventory(Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    received_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    glass_id = Column(Integer, ForeignKey('glasses.id'), nullable=False)
    
    owner = relationship("Glass")
