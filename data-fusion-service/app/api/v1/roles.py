"""
Data Fusion Hub Service - Roles API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.core.database import get_db
from app.models.role_api import Role, RoleCreate, RoleUpdate
from app.models.role_db import RoleDB

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Role])
async def get_roles(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    """Get all roles."""
    roles = db.query(RoleDB).offset(skip).limit(limit).all()
    return roles


@router.get("/{role_id}", response_model=Role)
async def get_role(role_id: str, db = Depends(get_db)):
    """Get a specific role by ID."""
    role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=Role)
async def create_role(role: RoleCreate, db = Depends(get_db)):
    """Create a new role."""
    db_role = RoleDB(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.put("/{role_id}", response_model=Role)
async def update_role(role_id: str, role_update: RoleUpdate, db = Depends(get_db)):
    """Update a specific role."""
    db_role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    for key, value in role_update.dict(exclude_unset=True).items():
        setattr(db_role, key, value)
        
    db.commit()
    db.refresh(db_role)
    return db_role


@router.delete("/{role_id}")
async def delete_role(role_id: str, db = Depends(get_db)):
    """Delete a specific role."""
    db_role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(db_role)
    db.commit()
    return {"message": "Role deleted successfully"}