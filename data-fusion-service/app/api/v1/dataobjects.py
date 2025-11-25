"""
Data Fusion Hub Service - Data Object API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.data_object import DataObjectCreate, DataObjectUpdate, DataObject
from app.models.data_object_bulk import DataObjectBulkCreate, DataObjectBulkResponse
from app.repositories.data_object_repository import DataObjectRepository
from app.repositories.data_field_repository import DataFieldRepository
from app.repositories.data_domain_repository import DataDomainRepository


router = APIRouter(prefix="/data-objects", tags=["Data Objects"])


@router.get("/", response_model=List[DataObject])
def list_data_objects(db: Session = Depends(get_db)):
    """Get all data objects."""
    repository = DataObjectRepository(db)
    return repository.get_all()


@router.get("/{id}", response_model=DataObject)
def get_data_object(id: str, db: Session = Depends(get_db)):
    """Get a data object by ID."""
    repository = DataObjectRepository(db)
    data_object = repository.get_by_id(id)
    if not data_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data object not found")
    return data_object


@router.post("/", response_model=DataObject)
def create_data_object(
    data_object_create: DataObjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new data object."""
    # Validate that the data domain exists
    domain_repo = DataDomainRepository(db)
    if not domain_repo.get_by_id(data_object_create.data_domain_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data domain not found"
        )
    
    repository = DataObjectRepository(db)
    
    # Check for duplicate full qualified name within the same domain
    existing = repository.get_by_full_qualified_name_and_domain(
        data_object_create.full_qualified_name,
        data_object_create.data_domain_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data object with this full qualified name already exists in the domain"
        )
    
    # Create the data object
    return repository.create(data_object_create, created_by="system")


@router.post("/bulk", response_model=List[DataObjectBulkResponse])
def create_data_objects_bulk(
    bulk_request: DataObjectBulkCreate,
    db: Session = Depends(get_db)
):
    """Create multiple data objects in a single request."""
    # Validate that the data domain exists
    domain_repo = DataDomainRepository(db)
    if not domain_repo.get_by_id(bulk_request.data_domain_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data domain not found"
        )
    
    # Validate all data objects first
    for i, data_object in enumerate(bulk_request.data_objects):
        if not data_object.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Data object at index {i} must have a name"
            )
        
        # Ensure data_fields is provided and not empty
        if not data_object.data_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Data object '{data_object.name}' must have data_fields specified"
            )
    
    # Create all data objects within a single transaction
    repository = DataObjectRepository(db)
    field_repository = DataFieldRepository(db)
    
    created_objects = []
    
    try:
        for data_object in bulk_request.data_objects:
            # Set the domain ID on each object to ensure consistency
            data_object_data = data_object.dict()
            data_object_data["data_domain_id"] = bulk_request.data_domain_id
            
            # Create the data object
            db_data_object = repository.create(data_object_data, created_by="system")
            
            # Create associated fields
            if hasattr(data_object, 'data_fields') and data_object.data_fields:
                created_fields = []
                for field in data_object.data_fields:
                    # Set the object_id to link this field to the parent data object
                    field_data = field.dict()
                    field_data["object_id"] = db_data_object.id
                    field_data["created_by"] = "system"
                    field_data["updated_by"] = "system"
                    
                    created_field = field_repository.create(field_data)
                    created_fields.append(created_field)
                
                # Create response object with fields
                temp_response_obj = DataObjectBulkResponse(
                    id=db_data_object.id,
                    name=db_data_object.name,
                    description=db_data_object.description,
                    type=db_data_object.type,
                    data_domain_id=db_data_object.data_domain_id,  # Include domain ID in response
                    created_at=db_data_object.created_at,
                    updated_at=db_data_object.updated_at,
                    data_fields=created_fields  # This will be the list of fields
                )
                
                created_objects.append(temp_response_obj)
            else:
                # Create response object without fields (should not happen due to validation above)
                temp_response_obj = DataObjectBulkResponse(
                    id=db_data_object.id,
                    name=db_data_object.name,
                    description=db_data_object.description,
                    type=db_data_object.type,
                    data_domain_id=db_data_object.data_domain_id,  # Include domain ID in response
                    created_at=db_data_object.created_at,
                    updated_at=db_data_object.updated_at,
                    data_fields=[]  # No fields
                )
                
                created_objects.append(temp_response_obj)
        
        return created_objects
        
    except Exception as e:
        # If any error occurs, the transaction will be automatically rolled back
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating data objects: {str(e)}"
        )


@router.put("/{id}", response_model=DataObject)
def update_data_object(
    id: str,
    data_object_update: DataObjectUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing data object."""
    repository = DataObjectRepository(db)
    
    # Check if the data object exists
    existing_data_object = repository.get_by_id(id)
    if not existing_data_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data object not found")
    
    # If updating domain ID, validate that it exists
    if data_object_update.data_domain_id and data_object_update.data_domain_id != existing_data_object.data_domain_id:
        domain_repo = DataDomainRepository(db)
        if not domain_repo.get_by_id(data_object_update.data_domain_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data domain not found"
            )
    
    # If updating full qualified name, check for duplicates in the same domain
    if data_object_update.full_qualified_name and data_object_update.full_qualified_name != existing_data_object.full_qualified_name:
        # Check if this new FQN already exists within the same domain
        existing = repository.get_by_full_qualified_name_and_domain(
            data_object_update.full_qualified_name,
            existing_data_object.data_domain_id  # Use current domain ID
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data object with this full qualified name already exists in the domain"
            )
    
    return repository.update(id, data_object_update, updated_by="system")


@router.delete("/{id}")
def delete_data_object(id: str, db: Session = Depends(get_db)):
    """Delete a data object."""
    repository = DataObjectRepository(db)
    success = repository.delete(id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data object not found")
    return {"message": "Data object deleted successfully"}