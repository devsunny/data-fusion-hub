"""
Data Fusion Hub Service - Authentication Tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import UserCreate
from app.repositories.concrete_user_repository import ConcreteUserRepository


@pytest.fixture(scope="module")
def test_client():
    """Create a test client for the application."""
    client = TestClient(app)
    return client


def test_login_endpoint_exists(test_client):
    """Test that the login endpoint exists and is accessible."""
    response = test_client.post("/auth/login")
    assert response.status_code == 422  # Expecting validation error, not auth error
    assert response.json()["detail"][0]["type"] == "missing"


def test_login_with_valid_credentials(test_client, db: Session):
    """Test login with valid credentials."""
    
    # First create a user for testing
    repository = ConcreteUserRepository(db)
    
    user_data = UserCreate(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="password123"
    )
    
    created_user = repository.create(user_data, "test_creator")
    
    # Now test login
    response = test_client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_invalid_credentials(test_client, db: Session):
    """Test login with invalid credentials."""
    
    # Test with wrong password
    response = test_client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_with_nonexistent_user(test_client):
    """Test login with non-existent user."""
    
    # Test with a user that doesn't exist
    response = test_client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "anyPassword"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"