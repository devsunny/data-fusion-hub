"""
Data Fusion Hub Service API - Configuration Settings
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Data Fusion Hub Service API"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/data_fusion_hub"
    
    # CORS settings  
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Server settings
    BACKEND_CORS_ORIGINS: List[str] = []
    
    class Config:
        case_sensitive = True

settings = Settings()