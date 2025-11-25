"""
Data Fusion Hub Service - User Role Request Database Model
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum
from app.core.database import Base


class UserRoleRequestBase(BaseModel):
    """Base user role request model with common fields."""
    user_id: str = Field(..., description="UUID of the requesting user")
    role_id: str = Field(..., description="UUID of the role being requested")  
    justification: str = Field(..., description="Reason for requesting the role")
    reason: Optional[str] = Field(None, description="Optional reason for approval/denial")


class UserRoleRequestCreate(UserRoleRequestBase):
    """Model for creating a new user role request."""
    pass


class UserRoleRequestUpdate(BaseModel):
    """Model for updating an existing user role request."""
    status: str
    reason: Optional[str] = None


class UserRoleRequestDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "user_role_requests"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: str = Column(String, nullable=False)
    role_id: str = Column(String, nullable=False)  
    justification: str = Column(Text, nullable=False)
    reason: Optional[str] = Column(Text)
    status: str = Column(String, nullable=False, default="pending")
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class UserRoleRequest(UserRoleRequestBase):
    """Model for returning a user role request (includes ID and timestamps)."""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True