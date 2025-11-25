"""
Data Fusion Hub Service - Role Approver Relationships Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from app.core.database import get_db
from app.models.role_approver_relationship_db import RoleApproverRelationshipDB, RoleApproverRelationshipCreate, RoleApproverRelationship
from app.models.role_db import RoleDB

router = APIRouter(
    prefix="/roles/{role_id}/approver-roles",
    tags=["Role Approver Relationships"],
    responses={404: {"description": "Not found"}},
)


@router.put("/", response_model=List[RoleApproverRelationship])
async def assign_approver_roles(
    role_id: str,
    approver_role_ids: List[str],
    db = Depends(get_db)
):
    """Assign one or more roles as approvers for a specific role."""
    
    # Validate that the target role exists
    target_role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not target_role:
        raise HTTPException(status_code=404, detail="Target role not found")
        
    # Validate that all approver roles exist and are different from target role
    for approver_role_id in approver_role_ids:
        if approver_role_id == role_id:
            raise HTTPException(
                status_code=400, 
                detail="Cannot assign a role to itself as an approver"
            )
        
        approver_role = db.query(RoleDB).filter(RoleDB.id == approver_role_id).first()
        if not approver_role:
            raise HTTPException(status_code=404, detail=f"Approver role with ID {approver_role_id} not found")
    
    # Delete existing relationships for this role
    db.query(RoleApproverRelationshipDB).filter(
        RoleApproverRelationshipDB.role_id == role_id
    ).delete()
    
    # Create new relationships
    created_relationships = []
    for approver_role_id in approver_role_ids:
        relationship = RoleApproverRelationshipDB(
            id=str(uuid.uuid4()),
            role_id=role_id,
            approver_role_id=approver_role_id,
            created_by="system",  # This would be replaced with actual user when auth is implemented
            updated_by="system"
        )
        db.add(relationship)
        db.commit()
        db.refresh(relationship)
        created_relationships.append(relationship)
    
    return created_relationships


@router.get("/", response_model=List[RoleApproverRelationship])
async def get_approver_roles(
    role_id: str,
    db = Depends(get_db)
):
    """Get all approver roles for a specific role."""
    
    # Validate that the target role exists
    target_role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not target_role:
        raise HTTPException(status_code=404, detail="Target role not found")
        
    relationships = db.query(RoleApproverRelationshipDB).filter(
        RoleApproverRelationshipDB.role_id == role_id
    ).all()
    
    return relationships


@router.delete("/{approver_role_id}")
async def remove_approver_role(
    role_id: str,
    approver_role_id: str,
    db = Depends(get_db)
):
    """Remove an approver role from a specific role."""
    
    # Validate that the target role exists
    target_role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not target_role:
        raise HTTPException(status_code=404, detail="Target role not found")
        
    # Find and delete the relationship
    relationship = db.query(RoleApproverRelationshipDB).filter(
        RoleApproverRelationshipDB.role_id == role_id,
        RoleApproverRelationshipDB.approver_role_id == approver_role_id
    ).first()
    
    if not relationship:
        raise HTTPException(status_code=404, detail="Role approver relationship not found")
        
    db.delete(relationship)
    db.commit()
    
    return {"message": "Approver role removed successfully"}