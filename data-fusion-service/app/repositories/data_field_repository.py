from sqlalchemy.orm import Session
from app.models.data_field import DataFieldDB, DataFieldCreate, DataFieldUpdate
from uuid import UUID

class DataFieldRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, data_field_data: dict) -> DataFieldDB:
        """Create a new data field"""
        # Create the database model instance
        data_field = DataFieldDB(**data_field_data)
        self.db_session.add(data_field)
        self.db_session.commit()
        self.db_session.refresh(data_field)
        return data_field
    
    def get_by_id(self, id: UUID) -> DataFieldDB:
        """Get data field by ID"""
        return self.db_session.query(DataFieldDB).filter(DataFieldDB.id == str(id)).first()
    
    def get_by_object_id(self, object_id: UUID) -> list[DataFieldDB]:
        """Get all data fields for a specific data object"""
        return self.db_session.query(DataFieldDB).filter(DataFieldDB.object_id == str(object_id)).all()
    
    def get_by_name_and_object_id(self, name: str, object_id: UUID) -> DataFieldDB:
        """Get data field by name and object_id combination"""
        return self.db_session.query(DataFieldDB).filter(
            DataFieldDB.name == name,
            DataFieldDB.object_id == str(object_id)
        ).first()
    
    def update(self, id: UUID, data_field_data: dict) -> DataFieldDB:
        """Update an existing data field"""
        data_field = self.get_by_id(id)
        if data_field:
            for key, value in data_field_data.items():
                setattr(data_field, key, value)
            self.db_session.commit()
            self.db_session.refresh(data_field)
        return data_field
    
    def delete(self, id: UUID) -> bool:
        """Delete a data field"""
        data_field = self.get_by_id(id)
        if data_field:
            self.db_session.delete(data_field)
            self.db_session.commit()
            return True
        return False