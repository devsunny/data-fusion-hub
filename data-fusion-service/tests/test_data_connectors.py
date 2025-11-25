"""
Data Fusion Hub Service - Data Connector Tests
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, engine
from app.models.data_connector import DataConnectorCreate, DataConnectorUpdate
from app.repositories.data_connector_repository import DataConnectorRepository

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
    """Create a data connector repository for testing."""
    return DataConnectorRepository(test_db)

def test_create_data_connector(repository):
    """Test creating a new data connector."""
    # Create test data
    data_connector_data = DataConnectorCreate(
        name="Test REST API",
        description="A test REST API endpoint",
        type="rest",
        configuration={
            "endpoint_url": "https://api.example.com",
            "timeout": 30
        },
        created_by="test_user"
    )
    
    # Create the data connector
    created = repository.create(data_connector_data, "test_user")
    
    # Verify it was created correctly
    assert created.id is not None
    assert created.name == "Test REST API"
    assert created.type == "rest"
    assert created.configuration["endpoint_url"] == "https://api.example.com"

def test_get_data_connector(repository):
    """Test retrieving a data connector by ID."""
    # Create test data first
    data_connector_data = DataConnectorCreate(
        name="Test SFTP Server",
        description="A test SFTP server",
        type="sftp", 
        configuration={
            "hostname": "sftp.example.com",
            "port": 22
        },
        created_by="test_user"
    )
    
    created = repository.create(data_connector_data, "test_user")
    
    # Retrieve it by ID
    retrieved = repository.get_by_id(created.id)
    
    assert retrieved is not None
    assert retrieved.name == "Test SFTP Server"

def test_update_data_connector(repository):
    """Test updating a data connector."""
    # Create test data first
    data_connector_data = DataConnectorCreate(
        name="Original Name",
        description="Original description",
        type="postgresql",
        configuration={
            "host": "localhost",
            "port": 5432
        },
        created_by="test_user"
    )
    
    created = repository.create(data_connector_data, "test_user")
    
    # Update it
    update_data = DataConnectorUpdate(
        name="Updated Name",
        description="Updated description",
        configuration={
            "host": "localhost", 
            "port": 5432,
            "database": "new_db"
        },
        updated_by="test_user"
    )
    
    updated = repository.update(created.id, update_data, "test_user")
    
    assert updated.name == "Updated Name"
    assert updated.description == "Updated description"

def test_delete_data_connector(repository):
    """Test deleting a data connector."""
    # Create test data first
    data_connector_data = DataConnectorCreate(
        name="To Delete",
        type="rest",
        configuration={
            "endpoint_url": "https://api.example.com"
        },
        created_by="test_user"
    )
    
    created = repository.create(data_connector_data, "test_user")
    
    # Delete it
    success = repository.delete(created.id)
    
    assert success is True
    
    # Verify it's gone
    deleted = repository.get_by_id(created.id)
    assert deleted is None

def test_get_all_data_connectors(repository):
    """Test getting all data connectors."""
    # Create multiple test data connectors
    data_connector1 = DataConnectorCreate(
        name="First API",
        type="rest",
        configuration={"endpoint_url": "https://api1.example.com"},
        created_by="test_user"
    )
    
    data_connector2 = DataConnectorCreate(
        name="Second API", 
        type="sftp",
        configuration={"hostname": "sftp.example.com"},
        created_by="test_user"
    )
    
    repository.create(data_connector1, "test_user")
    repository.create(data_connector2, "test_user")
    
    # Get all
    all_connectors = repository.get_all()
    
    assert len(all_connectors) >= 2  # May be more due to previous tests

if __name__ == "__main__":
    pytest.main([__file__, "-v"])