"""
Data Fusion Hub Service - Role API Models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    """Base role model with common fields."""
    name: str = Field(..., description="Human-readable name for the role")
    description: Optional[str] = Field(None, description="Description of the role purpose")

class RoleCreate(RoleBase):
    """Model for creating a new role."""
    pass

class RoleUpdate(BaseModel):
    """Model for updating an existing role."""
    name: Optional[str] = None
    description: Optional[str] = None

class RoleInDB(RoleBase):
    """Role model with database fields."""
    id: str
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Role(RoleInDB):
    """Model for returning a role (includes ID and timestamps)."""
    pass