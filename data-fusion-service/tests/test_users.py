"""
Data Fusion Hub Service - User Tests
"""

import pytest
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserUpdate
from app.repositories.concrete_user_repository import ConcreteUserRepository


def test_create_user(db: Session):
    """Test creating a new user."""
    repository = ConcreteUserRepository(db)
    
    # Create a user
    user_data = UserCreate(
        email="test@example.com",
        first_name="John",
        middle_name="Michael",
        last_name="Doe",
        password="password123"
    )
    
    created_user = repository.create(user_data, "test_creator")
    
    assert created_user.email == "test@example.com"
    assert created_user.first_name == "John"
    assert created_user.middle_name == "Michael"
    assert created_user.last_name == "Doe"
    assert created_user.id is not None
    assert len(created_user.id) > 0
    # Test that audit trail fields are present and populated
    assert created_user.created_by == "test_creator"
    assert created_user.updated_by == "test_creator"
    assert created_user.password_hash is not None


def test_get_user_by_id(db: Session):
    """Test retrieving a user by ID."""
    repository = ConcreteUserRepository(db)
    
    # First create a user
    user_data = UserCreate(
        email="user2@example.com",
        first_name="Jane",
        last_name="Smith"
    )
    
    created_user = repository.create(user_data, "test_creator")
    
    # Then retrieve it by ID
    retrieved_user = repository.get_by_id(created_user.id)
    
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.email == "user2@example.com"
    assert retrieved_user.created_by == "test_creator"
    assert retrieved_user.updated_by == "test_creator"


def test_get_user_by_email(db: Session):
    """Test retrieving a user by email."""
    repository = ConcreteUserRepository(db)
    
    # First create a user
    user_data = UserCreate(
        email="email@test.com",
        first_name="Bob",
        last_name="Johnson"
    )
    
    created_user = repository.create(user_data, "test_creator")
    
    # Then retrieve it by email
    retrieved_user = repository.get_by_email("email@test.com")
    
    assert retrieved_user is not None
    assert retrieved_user.email == "email@test.com"
    assert retrieved_user.id == created_user.id


def test_get_all_users(db: Session):
    """Test retrieving all users."""
    repository = ConcreteUserRepository(db)
    
    # Create a few users
    user_data1 = UserCreate(
        email="user1@example.com",
        first_name="Alice",
        last_name="Brown"
    )
    
    user_data2 = UserCreate(
        email="user2@example.com", 
        first_name="Charlie",
        last_name="Davis"
    )
    
    repository.create(user_data1, "creator1")
    repository.create(user_data2, "creator2")
    
    # Get all users
    all_users = repository.get_all()
    
    assert len(all_users) >= 2


def test_update_user(db: Session):
    """Test updating a user."""
    repository = ConcreteUserRepository(db)
    
    # Create a user
    user_data = UserCreate(
        email="update@example.com",
        first_name="Original",
        last_name="Name"
    )
    
    created_user = repository.create(user_data, "original_creator")
    
    # Update the user
    update_data = UserUpdate(
        email="updated@example.com",
        first_name="Updated",
        last_name="Name"
    )
    
    updated_user = repository.update(created_user.id, update_data, "updater")
    
    assert updated_user.email == "updated@example.com"
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    # Test that created_by remains unchanged but updated_by is updated
    assert updated_user.created_by == "original_creator"
    assert updated_user.updated_by == "updater"


def test_delete_user(db: Session):
    """Test deleting a user."""
    repository = ConcreteUserRepository(db)
    
    # Create a user
    user_data = UserCreate(
        email="delete@example.com",
        first_name="ToDelete",
        last_name="User"
    )
    
    created_user = repository.create(user_data, "deleter")
    
    # Delete the user
    success = repository.delete(created_user.id)
    
    assert success is True
    
    # Verify it's gone
    retrieved_user = repository.get_by_id(created_user.id)
    assert retrieved_user is None


def test_unique_email_enforcement(db: Session):
    """Test that email uniqueness is enforced."""
    repository = ConcreteUserRepository(db)
    
    # Create a user
    user_data = UserCreate(
        email="unique@example.com",
        first_name="Unique",
        last_name="User"
    )
    
    repository.create(user_data, "test_creator")
    
    # Try to create another user with the same email - should fail
    with pytest.raises(ValueError):
        duplicate_user_data = UserCreate(
            email="unique@example.com",
            first_name="Duplicate",
            last_name="User"
        )
        repository.create(duplicate_user_data, "test_creator")


def test_social_login_user(db: Session):
    """Test creating a user without password (social login scenario)."""
    repository = ConcreteUserRepository(db)
    
    # Create a social login user (no password)
    user_data = UserCreate(
        email="social@example.com",
        first_name="Social",
        last_name="User"
        # No password provided - for social login
    )
    
    created_user = repository.create(user_data, "social_creator")
    
    assert created_user.email == "social@example.com"
    assert created_user.password_hash is None  # Should be None for social users