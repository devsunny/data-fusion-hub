"""
Data Fusion Hub Service - Role Approver Relationship Model
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RoleApproverRelationshipBase(BaseModel):
    """Base role approver relationship model with common fields."""
    role_id: str = Field(..., description="UUID of the target role")
    approver_role_id: str = Field(..., description="UUID of the approver role")


class RoleApproverRelationshipCreate(RoleApproverRelationshipBase):
    """Model for creating a new role approver relationship."""
    pass


class RoleApproverRelationshipInDBBase(RoleApproverRelationshipBase):
    """Base role approver relationship model for database operations."""
    id: str = Field(..., description="UUID of the relationship")
    created_by: Optional[str] = Field(None, max_length=255)
    updated_by: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleApproverRelationship(RoleApproverRelationshipInDBBase):
    """Role approver relationship model for API responses."""
    pass