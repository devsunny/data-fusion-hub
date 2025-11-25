"""
Data Fusion Hub Service - User Model
"""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model for shared fields."""
    email: EmailStr = Field(..., max_length=255)
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """User model for creating new users."""
    password: Optional[str] = Field(None, min_length=6, max_length=255)


class UserUpdate(UserBase):
    """User model for updating existing users."""
    password: Optional[str] = Field(None, min_length=6, max_length=255)


class UserInDBBase(UserBase):
    """Base user model for database operations."""
    id: str = Field(..., description="UUID of the user")
    created_by: Optional[str] = Field(None, max_length=255)
    updated_by: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """User model for API responses."""
    password_hash: Optional[str] = Field(None, max_length=255)

    # In Pydantic v2, conversion is handled automatically by from_attributes=True configuration