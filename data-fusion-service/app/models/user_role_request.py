"""
Data Fusion Hub Service - User Role Request Model
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserRoleRequestBase(BaseModel):
    """Base user role request model with common fields."""
    user_id: str = Field(..., description="UUID of the requesting user")
    role_id: str = Field(..., description="UUID of the requested role")
    status: str = Field(..., description="Status of the request (pending/approved/rejected)")


class UserRoleRequestCreate(UserRoleRequestBase):
    """Model for creating a new user role request."""
    pass


class UserRoleRequestInDBBase(UserRoleRequestBase):
    """Base user role request model for database operations."""
    id: str = Field(..., description="UUID of the request")
    created_by: Optional[str] = Field(None, max_length=255)
    updated_by: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserRoleRequest(UserRoleRequestInDBBase):
    """User role request model for API responses."""
    pass