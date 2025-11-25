"""
Data Fusion Hub Service - Data Connector API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.data_connector import DataConnector, DataConnectorCreate, DataConnectorUpdate
from app.repositories.data_connector_repository import DataConnectorRepository

router = APIRouter(prefix="/dataconnectors", tags=["Data Connectors"])

# Pydantic model for pagination metadata
class PaginationMetadata(BaseModel):
    page: int
    size: int
    total: int
    pages: int

class PaginatedDataConnectorResponse(BaseModel):
    data: List[DataConnector]
    pagination: PaginationMetadata

@router.get("/", response_model=PaginatedDataConnectorResponse)
def list_data_connectors(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """Get all data connectors with pagination support."""
    
    repository = DataConnectorRepository(db)
    
    # Get total count
    total = len(repository.get_all())
    
    # Calculate offset and limit for database query
    skip = (page - 1) * size
    
    # For simplicity in this implementation, we'll get all items 
    # In a real system, you'd implement actual database pagination
    data_connectors = repository.get_all()
    
    # Apply pagination to the results
    start_idx = skip
    end_idx = min(skip + size, len(data_connectors))
    paginated_data = data_connectors[start_idx:end_idx]
    
    pages = (total + size - 1) // size
    
    return PaginatedDataConnectorResponse(
        data=paginated_data,
        pagination=PaginationMetadata(
            page=page,
            size=size,
            total=total,
            pages=pages
        )
    )

@router.post("/", response_model=DataConnector, status_code=status.HTTP_201_CREATED)
def create_data_connector(
    data_connector: DataConnectorCreate,
    db: Session = Depends(get_db),
    current_user: str = "test_user"  # In a real implementation, this would come from auth
):
    """Create a new data connector."""
    repository = DataConnectorRepository(db)
    
    try:
        created_data_connector = repository.create(data_connector, current_user)
        return created_data_connector
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create data connector: {str(e)}")

@router.get("/{id}", response_model=DataConnector)
def get_data_connector(
    id: str,
    db: Session = Depends(get_db)
):
    """Get a specific data connector by ID."""
    repository = DataConnectorRepository(db)
    data_connector = repository.get_by_id(id)
    
    if not data_connector:
        raise HTTPException(status_code=404, detail="Data connector not found")
    
    return data_connector

@router.put("/{id}", response_model=DataConnector)
def update_data_connector(
    id: str,
    data_connector_update: DataConnectorUpdate,
    db: Session = Depends(get_db),
    current_user: str = "test_user"  # In a real implementation, this would come from auth
):
    """Update an existing data connector."""
    repository = DataConnectorRepository(db)
    
    updated_data_connector = repository.update(id, data_connector_update, current_user)
    
    if not updated_data_connector:
        raise HTTPException(status_code=404, detail="Data connector not found")
    
    return updated_data_connector

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_connector(
    id: str,
    db: Session = Depends(get_db)
):
    """Delete a data connector."""
    repository = DataConnectorRepository(db)
    
    success = repository.delete(id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Data connector not found")