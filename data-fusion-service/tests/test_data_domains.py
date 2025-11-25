"""
Data Fusion Hub Service - Data Domain Tests
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, engine
from app.models.data_domain import DataDomainCreate, DataDomainUpdate
from app.repositories.data_domain_repository import DataDomainRepository

# Create a test database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="module")
def test_db():
    """Create a test database session."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new engine and session for testing
    test_engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Create tables in the test database
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def repository(test_db):
    """Create a data domain repository for testing."""
    return DataDomainRepository(test_db)

def test_create_data_domain(repository):
    """Test creating a new data domain."""
    # Create test data
    data_domain_data = DataDomainCreate(
        name="Test Data Domain",
        description="A test data domain for testing purposes",
        created_by="test_user"
    )
    
    # Create the data domain
    created = repository.create(data_domain_data, "test_user")
    
    # Verify it was created correctly
    assert created.id is not None
    assert created.name == "Test Data Domain"
    assert created.description == "A test data domain for testing purposes"

def test_get_data_domain(repository):
    """Test retrieving a data domain by ID."""
    # Create test data first
    data_domain_data = DataDomainCreate(
        name="Test SFTP Server",
        description="A test SFTP server",
        created_by="test_user"
    )
    
    created = repository.create(data_domain_data, "test_user")
    
    # Retrieve it by ID
    retrieved = repository.get_by_id(created.id)
    
    assert retrieved is not None
    assert retrieved.name == "Test SFTP Server"

def test_update_data_domain(repository):
    """Test updating a data domain."""
    # Create test data first
    data_domain_data = DataDomainCreate(
        name="Original Name",
        description="Original description",
        created_by="test_user"
    )
    
    created = repository.create(data_domain_data, "test_user")
    
    # Update it
    update_data = DataDomainUpdate(
        name="Updated Name",
        description="Updated description"
    )
    
    updated = repository.update(created.id, update_data, "test_user")
    
    assert updated.name == "Updated Name"
    assert updated.description == "Updated description"

def test_delete_data_domain(repository):
    """Test deleting a data domain."""
    # Create test data first
    data_domain_data = DataDomainCreate(
        name="To Delete",
        created_by="test_user"
    )
    
    created = repository.create(data_domain_data, "test_user")
    
    # Delete it
    success = repository.delete(created.id)
    
    assert success is True
    
    # Verify it's gone
    deleted = repository.get_by_id(created.id)
    assert deleted is None

def test_get_all_data_domains(repository):
    """Test getting all data domains."""
    # Create multiple test data domains
    data_domain1 = DataDomainCreate(
        name="First Domain",
        created_by="test_user"
    )
    
    data_domain2 = DataDomainCreate(
        name="Second Domain", 
        created_by="test_user"
    )
    
    repository.create(data_domain1, "test_user")
    repository.create(data_domain2, "test_user")
    
    # Get all
    all_domains = repository.get_all()
    
    assert len(all_domains) >= 2  # May be more due to previous tests

if __name__ == "__main__":
    pytest.main([__file__, "-v"])