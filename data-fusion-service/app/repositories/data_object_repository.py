"""
Data Fusion Hub Service - Data Object Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.data_object import DataObject, DataObjectCreate, DataObjectUpdate
from datetime import datetime, timezone


class DataObjectRepository:
    """Repository for data object operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[DataObject]:
        """Get all data objects."""
        return self.db.query(DataObject).all()
    
    def get_by_id(self, id: str) -> Optional[DataObject]:
        """Get a data object by ID."""
        return self.db.query(DataObject).filter(DataObject.id == id).first()
    
    def get_by_domain_id(self, domain_id: str) -> List[DataObject]:
        """Get all data objects for a specific domain."""
        return self.db.query(DataObject).filter(DataObject.data_domain_id == domain_id).all()
    
    def create(self, data_object_create: DataObjectCreate, created_by: str) -> DataObject:
        """Create a new data object."""
        # Set the creator and updater
        data_object_data = data_object_create.dict()
        data_object_data["created_by"] = created_by
        data_object_data["updated_by"] = created_by
        
        db_data_object = DataObject(**data_object_data)
        self.db.add(db_data_object)
        self.db.commit()
        self.db.refresh(db_data_object)
        return db_data_object
    
    def update(self, id: str, data_object_update: DataObjectUpdate, updated_by: str) -> Optional[DataObject]:
        """Update an existing data object."""
        db_data_object = self.get_by_id(id)
        if not db_data_object:
            return None
        
        # Update fields
        update_data = data_object_update.dict(exclude_unset=True)
        update_data["updated_by"] = updated_by
        update_data["updated_at"] = datetime.now(timezone.utc)
        
        for key, value in update_data.items():
            setattr(db_data_object, key, value)
        
        self.db.commit()
        self.db.refresh(db_data_object)
        return db_data_object
    
    def delete(self, id: str) -> bool:
        """Delete a data object."""
        db_data_object = self.get_by_id(id)
        if not db_data_object:
            return False
        
        self.db.delete(db_data_object)
        self.db.commit()
        return True
    
    def get_by_full_qualified_name_and_domain(self, full_qualified_name: str, domain_id: str) -> Optional[DataObject]:
        """Get a data object by its full qualified name within a specific domain."""
        return self.db.query(DataObject).filter(
            DataObject.full_qualified_name == full_qualified_name,
            DataObject.data_domain_id == domain_id
        ).first()