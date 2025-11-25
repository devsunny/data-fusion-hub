"""
Data Fusion Hub Service - Role Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.core.database import Base

class RoleBase(BaseModel):
    """Base role model with common fields."""
    name: str = Field(..., description="Human-readable name for the role")
    description: Optional[str] = Field(None, description="Description of the role purpose")

class RoleCreate(RoleBase):
    """Model for creating a new role."""
    pass

class RoleUpdate(BaseModel):
    """Model for updating an existing role."""
    name: Optional[str] = None
    description: Optional[str] = None

class RoleInDBBase(RoleBase):
    """Base role model for database operations."""
    id: str
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RoleDB(RoleInDBBase):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "roles"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String, nullable=False, unique=True)  # Unique constraint enforced at DB level
    description: Optional[str] = Column(Text)
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Role(RoleBase):
    """Model for returning a role (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True