"""
Data Fusion Hub Service - Login Model
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LoginBase(BaseModel):
    """Base login model for shared fields."""
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=255)


class LoginCreate(LoginBase):
    """Login model for creating new logins."""
    pass


class LoginInDBBase(LoginBase):
    """Base login model for database operations."""
    id: str = Field(..., description="UUID of the login")
    created_by: Optional[str] = Field(None, max_length=255)
    updated_by: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(LoginBase):
    """Login request model for API endpoints."""
    pass


class Token(BaseModel):
    """JWT Token response model."""
    access_token: str = Field(..., description='JWT access token')
    token_type: str = Field(default='bearer', description='Token type')


class Login(LoginInDBBase):
    """Login model for API responses."""
    pass