"""
Data Fusion Hub Service - User Repository Interface
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User, UserCreate, UserUpdate


class UserRepository:
    """Interface for user repository operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, user: UserCreate, created_by: Optional[str] = None) -> User:
        """
        Create a new user.
        
        Args:
            user: User data to create
            created_by: Identifier of the entity that created this user
            
        Returns:
            Created user object
        """
        raise NotImplementedError
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: UUID of the user to retrieve
            
        Returns:
            User if found, None otherwise
        """
        raise NotImplementedError
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: Email address of the user to retrieve
            
        Returns:
            User if found, None otherwise
        """
        raise NotImplementedError
    
    async def get_all(self) -> List[User]:
        """
        Get all users.
        
        Returns:
            List of all users
        """
        raise NotImplementedError
    
    async def update(self, user_id: str, user_update: UserUpdate, updated_by: Optional[str] = None) -> Optional[User]:
        """
        Update an existing user.
        
        Args:
            user_id: UUID of the user to update
            user_update: Updated user data
            updated_by: Identifier of the entity that updated this user
            
        Returns:
            Updated user if found, None otherwise
        """
        raise NotImplementedError
    
    async def delete(self, user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: UUID of the user to delete
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError