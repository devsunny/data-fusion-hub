"""
Data Fusion Hub Service - Role Model
"""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Base role model for shared fields."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class RoleCreate(RoleBase):
    """Role model for creating new roles."""
    pass


class RoleUpdate(RoleBase):
    """Role model for updating existing roles."""
    pass


class RoleInDBBase(RoleBase):
    """Base role model for database operations."""
    id: str = Field(..., description="UUID of the role")
    created_by: Optional[str] = Field(None, max_length=255)
    updated_by: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    """Role model for API responses."""
    pass