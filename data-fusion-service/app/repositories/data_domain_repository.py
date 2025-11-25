"""
Data Fusion Hub Service - Data Domain Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.data_domain import DataDomainDB, DataDomainCreate, DataDomainUpdate
from datetime import datetime, timezone


class DataDomainRepository:
    """Repository for data domain operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[DataDomainDB]:
        """Get all data domains."""
        return self.db.query(DataDomainDB).all()
    
    def get_by_id(self, id: str) -> Optional[DataDomainDB]:
        """Get a data domain by ID."""
        return self.db.query(DataDomainDB).filter(DataDomainDB.id == id).first()
    
    def create(self, data_domain_create: DataDomainCreate, created_by: str) -> DataDomainDB:
        """Create a new data domain."""
        # Create the database model instance
        db_data_domain = DataDomainDB(
            name=data_domain_create.name,
            description=data_domain_create.description,
            created_by=created_by,
            updated_by=created_by
        )
        
        self.db.add(db_data_domain)
        self.db.commit()
        self.db.refresh(db_data_domain)
        return db_data_domain
    
    def update(self, id: str, data_domain_update: DataDomainUpdate, updated_by: str) -> Optional[DataDomainDB]:
        """Update an existing data domain."""
        db_data_domain = self.get_by_id(id)
        if not db_data_domain:
            return None
        
        # Update fields
        if data_domain_update.name is not None:
            db_data_domain.name = data_domain_update.name
        if data_domain_update.description is not None:
            db_data_domain.description = data_domain_update.description
            
        db_data_domain.updated_by = updated_by
        db_data_domain.updated_at = datetime.now(timezone.utc)
        
        self.db.commit()
        self.db.refresh(db_data_domain)
        return db_data_domain
    
    def delete(self, id: str) -> bool:
        """Delete a data domain."""
        db_data_domain = self.get_by_id(id)
        if not db_data_domain:
            return False
        
        self.db.delete(db_data_domain)
        self.db.commit()
        return True