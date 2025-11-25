"""
Data Fusion Hub Service - Concrete User Repository Implementation
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User, UserCreate, UserUpdate
from app.models.user_db import UserDB
from app.repositories.user_repository import UserRepository
from app.utils.password_utils import hash_password


class ConcreteUserRepository(UserRepository):
    """Concrete implementation of user repository."""
    
    async def create(self, user: UserCreate, created_by: Optional[str] = None) -> User:
        """
        Create a new user.
        
        Args:
            user: User data to create
            created_by: Identifier of the entity that created this user
            
        Returns:
            Created user object
        """
        # Handle password hashing if provided
        password_hash = None
        if hasattr(user, 'password') and user.password:
            password_hash = hash_password(user.password)
        
        # Convert Pydantic model to database model
        db_user = UserDB(
            email=user.email,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            password_hash=password_hash,
            created_by=created_by,
            updated_by=created_by
        )
        
        self.db.add(db_user)
        try:
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"User with email '{user.email}' already exists")
        
        # Convert back to Pydantic model - now using automatic conversion
        return User.model_validate(db_user)
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: UUID of the user to retrieve
            
        Returns:
            User if found, None otherwise
        """
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        return User.model_validate(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: Email address of the user to retrieve
            
        Returns:
            User if found, None otherwise
        """
        db_user = self.db.query(UserDB).filter(UserDB.email == email).first()
        return User.model_validate(db_user) if db_user else None
    
    async def get_all(self) -> List[User]:
        """
        Get all users.
        
        Returns:
            List of all users
        """
        db_users = self.db.query(UserDB).all()
        # Convert each to Pydantic model using automatic conversion
        return [User.model_validate(user) for user in db_users]
    
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
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return None
        
        # Handle password hashing if provided in update
        password_hash = getattr(user_update, 'password', None)
        if password_hash is not None:
            password_hash = hash_password(password_hash)
        
        # Update fields
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        
        # Set updated_by field and password_hash if needed
        if updated_by is not None:
            db_user.updated_by = updated_by
        
        if password_hash is not None:
            db_user.password_hash = password_hash
            
        try:
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"User with email '{user_update.email}' already exists")
        
        return User.model_validate(db_user)
    
    async def delete(self, user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: UUID of the user to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True