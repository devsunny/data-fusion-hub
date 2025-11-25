"""
Data Fusion Hub Service - User Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.core.database import Base

class UserBase(BaseModel):
    """Base user model with common fields."""
    username: str = Field(..., description="Unique username for the user")
    email: str = Field(..., description="Email address of the user")
    full_name: str = Field(..., description="Full name of the user")

class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., description="Password for the user account")

class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "users"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username: str = Column(String, nullable=False, unique=True)  # Unique constraint enforced at DB level
    email: str = Column(String, nullable=False, unique=True)  # Unique constraint enforced at DB level
    full_name: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(UserBase):
    """Model for returning a user (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True