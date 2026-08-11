# app/models/user.py
# This file defines the Users table as a Python class.
# SQLAlchemy turns this class into real SQL table structure.
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meals = relationship("Meal", back_populates="owner" , cascade="all, delete-orphan")  # One-to-many relationship with Meal