"""
Data Fusion Hub Service API - Health Check Routes
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}