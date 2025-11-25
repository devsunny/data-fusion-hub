"""
Data Fusion Hub Service - Concrete Role Repository Implementation
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.role import Role, RoleCreate, RoleUpdate
from app.models.role_db import RoleDB
from app.repositories.role_repository import RoleRepository


class ConcreteRoleRepository(RoleRepository):
    """Concrete implementation of role repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, role: RoleCreate, created_by: Optional[str] = None) -> Role:
        """
        Create a new role.
        
        Args:
            role: Role data to create
            created_by: Identifier of the user/system that created the role
            
        Returns:
            Created role with generated ID
        """
        # Convert Pydantic model to database model
        db_role = RoleDB(
            name=role.name,
            description=role.description,
            created_by=created_by,
            updated_by=created_by
        )
        
        self.db.add(db_role)
        try:
            self.db.commit()
            self.db.refresh(db_role)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Role with name '{role.name}' already exists")
        
        # Convert back to Pydantic model using automatic conversion
        return Role.model_validate(db_role)
    
    async def get_by_id(self, role_id: str) -> Optional[Role]:
        """
        Get role by ID.
        
        Args:
            role_id: UUID of the role to retrieve
            
        Returns:
            Role if found, None otherwise
        """
        db_role = self.db.query(RoleDB).filter(RoleDB.id == role_id).first()
        return Role.model_validate(db_role) if db_role else None
    
    async def get_all(self) -> List[Role]:
        """
        Get all roles.
        
        Returns:
            List of all roles
        """
        db_roles = self.db.query(RoleDB).all()
        return [Role.model_validate(role) for role in db_roles]
    
    async def update(self, role_id: str, role_update: RoleUpdate, updated_by: Optional[str] = None) -> Optional[Role]:
        """
        Update an existing role.
        
        Args:
            role_id: UUID of the role to update
            role_update: Updated role data
            updated_by: Identifier of the user/system that updated the role
            
        Returns:
            Updated role if found, None otherwise
        """
        db_role = self.db.query(RoleDB).filter(RoleDB.id == role_id).first()
        if not db_role:
            return None
        
        # Update fields
        for key, value in role_update.dict(exclude_unset=True).items():
            setattr(db_role, key, value)
        
        # Set updated_by field
        if updated_by is not None:
            db_role.updated_by = updated_by
        
        try:
            self.db.commit()
            self.db.refresh(db_role)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Role with name '{role_update.name}' already exists")
        
        return Role.model_validate(db_role)
    
    async def delete(self, role_id: str) -> bool:
        """
        Delete a role.
        
        Args:
            role_id: UUID of the role to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_role = self.db.query(RoleDB).filter(RoleDB.id == role_id).first()
        if not db_role:
            return False
        
        self.db.delete(db_role)
        self.db.commit()
        return True
    
    async def get_by_name(self, name: str) -> Optional[Role]:
        """
        Get role by name.
        
        Args:
            name: Name of the role to retrieve
            
        Returns:
            Role if found, None otherwise
        """
        db_role = self.db.query(RoleDB).filter(RoleDB.name == name).first()
        return Role.model_validate(db_role) if db_role else None