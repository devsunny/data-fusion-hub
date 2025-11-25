"""
Data Fusion Hub Service - Role Approver Relationship Database Model
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, DateTime
from app.core.database import Base


class RoleApproverRelationshipBase(BaseModel):
    """Base role approver relationship model with common fields."""
    role_id: str = Field(..., description="UUID of the target role")
    approver_role_id: str = Field(..., description="UUID of the approver role")


class RoleApproverRelationshipCreate(RoleApproverRelationshipBase):
    """Model for creating a new role approver relationship."""
    pass


class RoleApproverRelationshipDB(Base):
    """SQLAlchemy model for database persistence."""
    __tablename__ = "role_approver_relationships"
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role_id: str = Column(String, nullable=False)
    approver_role_id: str = Column(String, nullable=False)
    created_by: str = Column(String, nullable=False)
    updated_by: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class RoleApproverRelationship(RoleApproverRelationshipBase):
    """Model for returning a role approver relationship (includes ID and timestamps)."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True