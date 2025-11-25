"""
Data Fusion Hub Service - Data Domain Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.core.database import Base

class DataDomainBase(BaseModel):
    """Base data domain model with common fields."""
    name: str = Field(..., description="Human-readable name for the data domain")
    description: Optional[str] = Field(None, description="Description of the data domain purpose")

class DataDomainCreate(DataDomainBase):
    """Model for creating a new data domain."""
    pass

class DataDomainUpdate(BaseModel):
    """Model for updating an existing data domain."""
    name: Optional[str] = None
    description: Optional[str] = None

class DataDomainDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "data_domains"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String, nullable=False, unique=True)  # Unique constraint enforced at DB level
    description: Optional[str] = Column(Text)
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DataDomain(DataDomainBase):
    """Model for returning a data domain (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True