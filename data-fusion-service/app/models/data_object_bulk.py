"""
Data Fusion Hub Service - Data Object Bulk Models
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer, ForeignKey, Boolean, UniqueConstraint
from app.core.database import Base

# Import the existing models to extend them
from app.models.data_object import DataObjectBase


class DataFieldCreateBulk(BaseModel):
    """Model for creating a new data field as part of bulk operation."""
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


class DataObjectCreateBulk(DataObjectBase):
    """Model for creating a new data object as part of bulk operation."""
    # Remove data_domain_id from here since it's at the global level now
    data_fields: List[DataFieldCreateBulk] = Field(..., description="List of data fields to create with this data object")


class DataObjectBulkResponse(DataObjectBase):
    """Model for returning a data object in bulk response (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime
    # Include the associated data fields in the response
    data_fields: List[DataFieldCreateBulk] = Field(..., description="List of data fields associated with this data object")


class DataObjectBulkCreate(BaseModel):
    """Model for bulk creating multiple data objects."""
    data_domain_id: str = Field(..., description="ID of the data domain these objects belong to")
    data_objects: List[DataObjectCreateBulk] = Field(..., description="List of data objects to create")