"""
Data Fusion Hub Service - Data Field Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer, ForeignKey, Boolean, UniqueConstraint
from app.core.database import Base

class DataFieldBase(BaseModel):
    """Base data field model with common fields."""
    name: str = Field(..., description="Human-readable name for the data field")
    description: Optional[str] = Field(None, description="Description of the data field purpose")
    type: str = Field(..., description="Type of data field (string, integer, float, etc.)")
    is_required: bool = Field(False, description="Whether this field is required")
    ansi_data_type: Optional[str] = Field(None, description="ANSI data type for the field")
    display_name: Optional[str] = Field(None, description="Display name for the field")
    max_char_length: Optional[int] = Field(None, description="Maximum character length for string fields")
    min_char_length: Optional[int] = Field(None, description="Minimum character length for string fields")
    numerical_precision: Optional[int] = Field(None, description="Numerical precision for numeric fields")
    numerical_scale: Optional[int] = Field(None, description="Numerical scale for numeric fields")

class DataFieldCreate(DataFieldBase):
    """Model for creating a new data field."""
    pass

class DataFieldUpdate(BaseModel):
    """Model for updating an existing data field."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    is_required: Optional[bool] = None
    ansi_data_type: Optional[str] = None
    display_name: Optional[str] = None
    max_char_length: Optional[int] = None
    min_char_length: Optional[int] = None
    numerical_precision: Optional[int] = None
    numerical_scale: Optional[int] = None

class DataFieldDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "data_fields"
    
    # UUID primary key
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key to data object
    object_id: str = Column(String, ForeignKey("data_objects.id"), nullable=False)
    
    # Fields for the data field
    name: str = Column(String, nullable=False)
    description: Optional[str] = Column(Text)
    type: str = Column(String, nullable=False)  # e.g., 'string', 'integer', 'float'
    is_required: bool = Column(Boolean, nullable=False, default=False)  # Changed to Boolean for proper SQL type
    ansi_data_type: Optional[str] = Column(String)
    display_name: Optional[str] = Column(String)
    max_char_length: Optional[int] = Column(Integer)
    min_char_length: Optional[int] = Column(Integer)
    numerical_precision: Optional[int] = Column(Integer)
    numerical_scale: Optional[int] = Column(Integer)
    
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Composite unique constraint on (name, object_id)
    __table_args__ = (
        UniqueConstraint('name', 'object_id', name='uq_name_object_id'),
    )

class DataField(DataFieldBase):
    """Model for returning a data field (includes ID and timestamps)."""
    id: str
    object_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True