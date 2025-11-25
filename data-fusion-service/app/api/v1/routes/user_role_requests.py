"""
Data Fusion Hub Service - User Role Request Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from app.core.database import get_db
from app.models.user_role_request_db import UserRoleRequestDB, UserRoleRequestCreate, UserRoleRequestUpdate, UserRoleRequest
from app.models.role_approver_relationship_db import RoleApproverRelationshipDB
from app.models.user_db import UserDB
from app.models.role_db import RoleDB

router = APIRouter(
    prefix="/user-role-requests",
    tags=["User Role Requests"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserRoleRequest)
async def create_user_role_request(
    request: UserRoleRequestCreate,
    db = Depends(get_db)
):
    """Submit a new role request."""
    
    # Check if the requested role is public (not allowed)
    role = db.query(RoleDB).filter(RoleDB.id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role.name == "public":
        raise HTTPException(
            status_code=400, 
            detail="Cannot request membership in the public role"
        )
        
    # Check if user exists
    user = db.query(UserDB).filter(UserDB.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Create the user role request
    db_request = UserRoleRequestDB(**request.dict(), id=str(uuid.uuid4()))
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return db_request


@router.get("/", response_model=List[UserRoleRequest])
async def get_user_role_requests(
    user_id: str,
    db = Depends(get_db)
):
    """Get all role requests for a specific user."""
    requests = db.query(UserRoleRequestDB).filter(
        UserRoleRequestDB.user_id == user_id
    ).all()
    
    return requests


@router.get("/{request_id}", response_model=UserRoleRequest)
async def get_user_role_request(
    request_id: str,
    db = Depends(get_db)
):
    """Get a specific role request by ID."""
    request = db.query(UserRoleRequestDB).filter(
        UserRoleRequestDB.id == request_id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="User role request not found")
        
    return request


@router.put("/{request_id}/approve")
async def approve_user_role_request(
    request_id: str,
    update_data: UserRoleRequestUpdate,
    db = Depends(get_db)
):
    """Approve a user role request."""
    
    # Validate that the status is approved
    if update_data.status != "approved":
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'approved'")
        
    # Get the existing request
    db_request = db.query(UserRoleRequestDB).filter(
        UserRoleRequestDB.id == request_id
    ).first()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="User role request not found")
        
    # Update the request status and reason
    db_request.status = update_data.status
    if update_data.reason is not None:
        db_request.reason = update_data.reason
        
    db.commit()
    db.refresh(db_request)
    
    return {"message": "Role request approved successfully", "request_id": request_id}


@router.put("/{request_id}/deny")
async def deny_user_role_request(
    request_id: str,
    update_data: UserRoleRequestUpdate,
    db = Depends(get_db)
):
    """Deny a user role request."""
    
    # Validate that the status is denied
    if update_data.status != "denied":
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'denied'")
        
    # Get the existing request
    db_request = db.query(UserRoleRequestDB).filter(
        UserRoleRequestDB.id == request_id
    ).first()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="User role request not found")
        
    # Update the request status and reason
    db_request.status = update_data.status
    if update_data.reason is not None:
        db_request.reason = update_data.reason
        
    db.commit()
    db.refresh(db_request)
    
    return {"message": "Role request denied successfully", "request_id": request_id}