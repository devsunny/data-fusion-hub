"""
Data Fusion Hub Service - Data Object Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from app.core.database import Base

class DataObjectBase(BaseModel):
    """Base data object model with common fields."""
    name: str = Field(..., description="Human-readable name for the data object")
    description: Optional[str] = Field(None, description="Description of the data object purpose")
    type: str = Field(..., description="Type of data object (table, view, etc.)")
    data_domain_id: str = Field(..., description="ID of the data domain this object belongs to")

class DataObjectCreate(DataObjectBase):
    """Model for creating a new data object."""
    pass

class DataObjectUpdate(BaseModel):
    """Model for updating an existing data object."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    data_domain_id: Optional[str] = None

class DataObjectDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "data_objects"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String, nullable=False)
    description: Optional[str] = Column(Text)
    type: str = Column(String, nullable=False)  # e.g., 'table', 'view'
    data_domain_id: str = Column(String, ForeignKey("data_domains.id"), nullable=False)
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DataObject(DataObjectBase):
    """Model for returning a data object (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True