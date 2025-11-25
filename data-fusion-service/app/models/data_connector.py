"""
Data Fusion Hub Service - Data Connector Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.core.database import Base

class DataConnectorBase(BaseModel):
    """Base data connector model with common fields."""
    name: str = Field(..., description="Human-readable name for the data connector")
    description: Optional[str] = Field(None, description="Description of the data connector purpose")
    type: str = Field(..., description="Type of data connector (rest, sftp, postgresql, etc.)")
    configuration: Dict[str, Any] = Field(..., description="Configuration parameters specific to the data connector type")
    authentication: Optional[Dict[str, Any]] = Field(None, description="Authentication configuration for the data connector")

class DataConnectorCreate(DataConnectorBase):
    """Model for creating a new data connector."""
    pass

class DataConnectorUpdate(BaseModel):
    """Model for updating an existing data connector."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    authentication: Optional[Dict[str, Any]] = None

class DataConnectorDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "data_connectors"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String, nullable=False)
    description: Optional[str] = Column(Text)
    type: str = Column(String, nullable=False)  # e.g., 'rest', 'sftp', 'postgresql'
    configuration: Dict[str, Any] = Column(JSON, nullable=False)  # Store as JSON
    authentication: Optional[Dict[str, Any]] = Column(JSON)  # Store as JSON
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DataConnector(DataConnectorBase):
    """Model for returning a data connector (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True