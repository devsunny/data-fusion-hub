"""
Data Fusion Hub Service - User API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User, UserCreate, UserUpdate
from app.models.login import LoginRequest, Token
from app.repositories.concrete_user_repository import ConcreteUserRepository
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

def get_current_user_identifier(request: Request) -> str:
    """
    Get the identifier of the current user.
    
    In a real implementation, this would extract from authentication context,
    such as JWT token claims or session data.
    
    For demonstration purposes, we'll use a mock value.
    """
    # Mock implementation - in reality this would come from auth context
    return "system_user"

@router.post("/login", response_model=Token)
async def login_for_access_token(
    request_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT access token.
    
    Args:
        request_data: Login credentials (email and password)
        db: Database session
        
    Returns:
        Token object with access_token and token_type
        
    Raises:
        HTTPException: 401 Unauthorized if authentication fails
    """
    # In a real implementation, you would fetch the user from database by email
    # For now, we'll demonstrate with mock logic
    
    repository = ConcreteUserRepository(db)
    
    # This is where you'd normally query the database for the user
    # For demonstration purposes, let's assume we have a way to get the user
    try:
        # Mock implementation - in real app this would be actual DB lookup
        # Let's say we're looking up by email and checking password
        
        # This is just an example - you'd need to implement proper database logic here
        users = await repository.get_all()
        
        # Find user with matching email (this is a simplified approach)
        user = None
        for u in users:
            if u.email == request_data.email:
                user = u
                break
                
        if not user or not verify_password(request_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Create access token with user identifier
        access_token_expires = timedelta(minutes=30)
        token_data = {"sub": user.email}
        access_token = create_access_token(
            data=token_data, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    
    Args:
        user: User data to create
        request: HTTP request object for authentication context
        db: Database session
        
    Returns:
        Created user with generated UUID and provenance information
    """
    try:
        # Get the current user identifier from auth context
        created_by = get_current_user_identifier(request)
        
        repository = ConcreteUserRepository(db)
        created_user = await repository.create(user, created_by)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[User])
async def get_users(
    db: Session = Depends(get_db)
):
    """
    Get all users.
    
    Args:
        db: Database session
        
    Returns:
        List of all users
    """
    repository = ConcreteUserRepository(db)
    return await repository.get_all()

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a user by ID.
    
    Args:
        user_id: UUID of the user to retrieve
        db: Database session
        
    Returns:
        User if found, raises 404 if not found
    """
    repository = ConcreteUserRepository(db)
    user = await repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Update an existing user.
    
    Args:
        user_id: UUID of the user to update
        user_update: Updated user data
        request: HTTP request object for authentication context
        db: Database session
        
    Returns:
        Updated user if found, raises 404 if not found
    """
    try:
        # Get the current user identifier from auth context
        updated_by = get_current_user_identifier(request)
        
        repository = ConcreteUserRepository(db)
        updated_user = await repository.update(user_id, user_update, updated_by)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a user.
    
    Args:
        user_id: UUID of the user to delete
        db: Database session
        
    Returns:
        None if successful, raises 404 if not found
    """
    repository = ConcreteUserRepository(db)
    success = await repository.delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")