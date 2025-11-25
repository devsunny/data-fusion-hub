"""
Data Fusion Hub Service - Data Connector Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.data_connector import DataConnectorDB, DataConnectorCreate, DataConnectorUpdate
from datetime import datetime, timezone


class DataConnectorRepository:
    """Repository for data connector operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[DataConnectorDB]:
        """Get all data connectors."""
        return self.db.query(DataConnectorDB).all()
    
    def get_by_id(self, id: str) -> Optional[DataConnectorDB]:
        """Get a data connector by ID."""
        return self.db.query(DataConnectorDB).filter(DataConnectorDB.id == id).first()
    
    def create(self, data_connector_create: DataConnectorCreate, created_by: str) -> DataConnectorDB:
        """Create a new data connector."""
        # Create the database model instance
        db_data_connector = DataConnectorDB(
            name=data_connector_create.name,
            description=data_connector_create.description,
            type=data_connector_create.type,
            configuration=data_connector_create.configuration,
            authentication=data_connector_create.authentication,
            created_by=created_by,
            updated_by=created_by
        )
        
        self.db.add(db_data_connector)
        self.db.commit()
        self.db.refresh(db_data_connector)
        return db_data_connector
    
    def update(self, id: str, data_connector_update: DataConnectorUpdate, updated_by: str) -> Optional[DataConnectorDB]:
        """Update an existing data connector."""
        db_data_connector = self.get_by_id(id)
        if not db_data_connector:
            return None
        
        # Update fields
        if data_connector_update.name is not None:
            db_data_connector.name = data_connector_update.name
        if data_connector_update.description is not None:
            db_data_connector.description = data_connector_update.description
        if data_connector_update.type is not None:
            db_data_connector.type = data_connector_update.type
        if data_connector_update.configuration is not None:
            db_data_connector.configuration = data_connector_update.configuration
        if data_connector_update.authentication is not None:
            db_data_connector.authentication = data_connector_update.authentication
            
        db_data_connector.updated_by = updated_by
        db_data_connector.updated_at = datetime.now(timezone.utc)
        
        self.db.commit()
        self.db.refresh(db_data_connector)
        return db_data_connector
    
    def delete(self, id: str) -> bool:
        """Delete a data connector."""
        db_data_connector = self.get_by_id(id)
        if not db_data_connector:
            return False
        
        self.db.delete(db_data_connector)
        self.db.commit()
        return True