from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.data_field import DataField, DataFieldCreate, DataFieldUpdate
from src.repositories.data_field_repository import DataFieldRepository
from uuid import UUID

router = APIRouter(prefix="/data-fields", tags=["Data Fields"])

@router.post("/", response_model=DataField)
def create_data_field(
    data_field: DataFieldCreate,
    db: Session = Depends(get_db)
):
    """Create a new data field"""
    try:
        repo = DataFieldRepository(db)
        return repo.create(data_field.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=DataField)
def get_data_field(
    id: UUID,
    db: Session = Depends(get_db)
):
    """Get a data field by ID"""
    repo = DataFieldRepository(db)
    data_field = repo.get_by_id(id)
    if not data_field:
        raise HTTPException(status_code=404, detail="Data field not found")
    return data_field

@router.get("/object/{object_id}", response_model=list[DataField])
def get_data_fields_by_object(
    object_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all data fields for a specific data object"""
    repo = DataFieldRepository(db)
    return repo.get_by_object_id(object_id)

@router.put("/{id}", response_model=DataField)
def update_data_field(
    id: UUID,
    data_field_update: DataFieldUpdate,
    db: Session = Depends(get_db)
):
    """Update a data field"""
    repo = DataFieldRepository(db)
    updated_data_field = repo.update(id, data_field_update.dict(exclude_unset=True))
    if not updated_data_field:
        raise HTTPException(status_code=404, detail="Data field not found")
    return updated_data_field

@router.delete("/{id}", response_model=DataField)
def delete_data_field(
    id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a data field"""
    repo = DataFieldRepository(db)
    if not repo.delete(id):
        raise HTTPException(status_code=404, detail="Data field not found")
    return {"message": "Data field deleted successfully"}