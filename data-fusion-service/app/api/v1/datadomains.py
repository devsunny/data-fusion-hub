"""
Data Fusion Hub Service - Data Domain API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.data_domain import DataDomain, DataDomainCreate, DataDomainUpdate
from app.repositories.data_domain_repository import DataDomainRepository

router = APIRouter(prefix="/datadomains", tags=["Data Domains"])

# Pydantic model for pagination metadata
class PaginationMetadata(BaseModel):
    page: int
    size: int
    total: int
    pages: int

class PaginatedDataDomainResponse(BaseModel):
    data: List[DataDomain]
    pagination: PaginationMetadata

@router.get("/", response_model=PaginatedDataDomainResponse)
def list_data_domains(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """Get all data domains with pagination support."""
    
    repository = DataDomainRepository(db)
    
    # Get total count
    total = len(repository.get_all())
    
    # Calculate offset and limit for database query
    skip = (page - 1) * size
    
    # For simplicity in this implementation, we'll get all items 
    # In a real system, you'd implement actual database pagination
    data_domains = repository.get_all()
    
    # Apply pagination to the results
    start_idx = skip
    end_idx = min(skip + size, len(data_domains))
    paginated_data = data_domains[start_idx:end_idx]
    
    pages = (total + size - 1) // size
    
    return PaginatedDataDomainResponse(
        data=paginated_data,
        pagination=PaginationMetadata(
            page=page,
            size=size,
            total=total,
            pages=pages
        )
    )

@router.post("/", response_model=DataDomain, status_code=status.HTTP_201_CREATED)
def create_data_domain(
    data_domain: DataDomainCreate,
    db: Session = Depends(get_db),
    current_user: str = "test_user"  # In a real implementation, this would come from auth
):
    """Create a new data domain."""
    repository = DataDomainRepository(db)
    
    try:
        created_data_domain = repository.create(data_domain, current_user)
        return created_data_domain
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create data domain: {str(e)}")

@router.get("/{id}", response_model=DataDomain)
def get_data_domain(
    id: str,
    db: Session = Depends(get_db)
):
    """Get a specific data domain by ID."""
    repository = DataDomainRepository(db)
    data_domain = repository.get_by_id(id)
    
    if not data_domain:
        raise HTTPException(status_code=404, detail="Data domain not found")
    
    return data_domain

@router.put("/{id}", response_model=DataDomain)
def update_data_domain(
    id: str,
    data_domain_update: DataDomainUpdate,
    db: Session = Depends(get_db),
    current_user: str = "test_user"  # In a real implementation, this would come from auth
):
    """Update an existing data domain."""
    repository = DataDomainRepository(db)
    
    updated_data_domain = repository.update(id, data_domain_update, current_user)
    
    if not updated_data_domain:
        raise HTTPException(status_code=404, detail="Data domain not found")
    
    return updated_data_domain

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_domain(
    id: str,
    db: Session = Depends(get_db)
):
    """Delete a data domain."""
    repository = DataDomainRepository(db)
    
    success = repository.delete(id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Data domain not found")