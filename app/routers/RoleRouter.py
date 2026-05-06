from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.RoleCrud import get_role, get_roles, create_role, update_role, delete_role
from app.schemas.RoleSchema import RoleCreate, RoleUpdate, RoleResponse, RoleBase
from app.models.RoleModel import Role
from app.crud.RoleCrud import get_all_rolesDD
from app.utils.UserAuthUtils import verify_access_token

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# Create role
@router.post("/create", response_model=RoleResponse)
def api_create_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    existing = db.query(Role).filter(Role.role_name == role_in.role_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    return create_role(db, role_in)

# Get all roles
@router.get("/get-role", response_model=List[RoleResponse])
def api_get_roles(db: Session = Depends(get_db)):
    return get_roles(db)

# Get role by ID
@router.get("/{role_id}", response_model=RoleResponse)
def api_get_role(role_id: int, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Update role
@router.put("/{role_id}", response_model=RoleResponse)
def api_update_role(role_id: int, role_in: RoleUpdate, db: Session = Depends(get_db)):
    role = update_role(db, role_id, role_in)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Delete role (soft delete)
@router.delete("/{role_id}")
def api_delete_role(role_id: int, db: Session = Depends(get_db)):
    success = delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"detail": "Role deleted successfully"}



@router.get("DD", response_model=List[RoleBase], summary="Get all roles")
def fetch_all_roles(
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
):
    try:
        roles = get_all_rolesDD(db)
        return roles  # ✅ JSON serialized automatically
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
