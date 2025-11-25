"""
Data Fusion Hub Service - Authentication API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.login import LoginRequest, Token
from app.repositories.concrete_user_repository import ConcreteUserRepository
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

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
    
    repository = ConcreteUserRepository(db)
    
    try:
        # This is where you'd normally query the database for the user
        # For demonstration purposes, let's assume we have a way to get the user
        
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
        from datetime import timedelta
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
