"""
Data Fusion Hub Service - Role Repository Interface
"""

from typing import List, Optional
from uuid import UUID

from app.models.role import Role, RoleCreate, RoleUpdate


class RoleRepository:
    """Interface for role operations."""
    
    async def create(self, role: RoleCreate) -> Role:
        """
        Create a new role.
        
        Args:
            role: Role data to create
            
        Returns:
            Created role with generated ID
        """
        raise NotImplementedError
    
    async def get_by_id(self, role_id: str) -> Optional[Role]:
        """
        Get role by ID.
        
        Args:
            role_id: UUID of the role to retrieve
            
        Returns:
            Role if found, None otherwise
        """
        raise NotImplementedError
    
    async def get_all(self) -> List[Role]:
        """
        Get all roles.
        
        Returns:
            List of all roles
        """
        raise NotImplementedError
    
    async def update(self, role_id: str, role_update: RoleUpdate) -> Optional[Role]:
        """
        Update an existing role.
        
        Args:
            role_id: UUID of the role to update
            role_update: Updated role data
            
        Returns:
            Updated role if found, None otherwise
        """
        raise NotImplementedError
    
    async def delete(self, role_id: str) -> bool:
        """
        Delete a role.
        
        Args:
            role_id: UUID of the role to delete
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError
    
    async def get_by_name(self, name: str) -> Optional[Role]:
        """
        Get role by name.
        
        Args:
            name: Name of the role to retrieve
            
        Returns:
            Role if found, None otherwise
        """
        raise NotImplementedError