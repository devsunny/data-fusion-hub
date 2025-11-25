"""
Data Fusion Hub Service - Role Tests
"""

import pytest
from sqlalchemy.orm import Session
from app.models.role import RoleCreate, RoleUpdate
from app.repositories.concrete_role_repository import ConcreteRoleRepository


def test_create_role(db: Session):
    """Test creating a new role."""
    repository = ConcreteRoleRepository(db)
    
    # Create a role
    role_data = RoleCreate(
        name="test_role",
        description="A test role for testing purposes"
    )
    
    created_role = repository.create(role_data, "test_user")
    
    assert created_role.name == "test_role"
    assert created_role.description == "A test role for testing purposes"
    assert created_role.id is not None
    assert len(created_role.id) > 0
    # Test that new fields are present and populated
    assert created_role.created_by == "test_user"
    assert created_role.updated_by == "test_user"


def test_get_role_by_id(db: Session):
    """Test retrieving a role by ID."""
    repository = ConcreteRoleRepository(db)
    
    # First create a role
    role_data = RoleCreate(name="test_role_2", description="Another test role")
    created_role = repository.create(role_data, "test_user_2")
    
    # Then retrieve it by ID
    retrieved_role = repository.get_by_id(created_role.id)
    
    assert retrieved_role is not None
    assert retrieved_role.id == created_role.id
    assert retrieved_role.name == "test_role_2"
    assert retrieved_role.created_by == "test_user_2"
    assert retrieved_role.updated_by == "test_user_2"


def test_get_all_roles(db: Session):
    """Test retrieving all roles."""
    repository = ConcreteRoleRepository(db)
    
    # Create a few roles
    role_data1 = RoleCreate(name="role_1", description="First role")
    role_data2 = RoleCreate(name="role_2", description="Second role")
    
    repository.create(role_data1, "user1")
    repository.create(role_data2, "user2")
    
    # Get all roles
    all_roles = repository.get_all()
    
    assert len(all_roles) >= 2


def test_update_role(db: Session):
    """Test updating a role."""
    repository = ConcreteRoleRepository(db)
    
    # Create a role
    role_data = RoleCreate(name="old_name", description="Old description")
    created_role = repository.create(role_data, "original_user")
    
    # Update the role
    update_data = RoleUpdate(
        name="new_name",
        description="New description"
    )
    
    updated_role = repository.update(created_role.id, update_data, "updating_user")
    
    assert updated_role.name == "new_name"
    assert updated_role.description == "New description"
    # Test that created_by remains unchanged but updated_by is updated
    assert updated_role.created_by == "original_user"
    assert updated_role.updated_by == "updating_user"


def test_delete_role(db: Session):
    """Test deleting a role."""
    repository = ConcreteRoleRepository(db)
    
    # Create a role
    role_data = RoleCreate(name="delete_test", description="To be deleted")
    created_role = repository.create(role_data, "deleting_user")
    
    # Delete the role
    success = repository.delete(created_role.id)
    
    assert success is True
    
    # Verify it's gone
    retrieved_role = repository.get_by_id(created_role.id)
    assert retrieved_role is None


def test_unique_role_name(db: Session):
    """Test that role names must be unique."""
    repository = ConcreteRoleRepository(db)
    
    # Create a role
    role_data = RoleCreate(name="unique_role", description="Unique role")
    repository.create(role_data, "test_user")
    
    # Try to create another role with the same name - should fail
    with pytest.raises(ValueError):
        duplicate_role_data = RoleCreate(name="unique_role", description="Duplicate role")
        repository.create(duplicate_role_data, "test_user")


def test_get_role_by_name(db: Session):
    """Test retrieving a role by name."""
    repository = ConcreteRoleRepository(db)
    
    # Create a role
    role_data = RoleCreate(name="name_test", description="Name test role")
    created_role = repository.create(role_data, "test_user")
    
    # Retrieve by name
    retrieved_role = repository.get_by_name("name_test")
    
    assert retrieved_role is not None
    assert retrieved_role.id == created_role.id
    assert retrieved_role.name == "name_test"
    assert retrieved_role.created_by == "test_user"
    assert retrieved_role.updated_by == "test_user"