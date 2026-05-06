from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.RoleModel import Role
from app.schemas.RoleSchema import RoleCreate, RoleUpdate
from typing import List, Dict
from sqlalchemy import text

def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.role_id == role_id, Role.is_deleted == False).first()

def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    """Fetch role by id (used during login)"""
    return get_role(db, role_id)

def get_role_by_name(db: Session, role_name: str) -> Optional[Role]:
    """Fetch role by name (used during registration)"""
    return db.query(Role).filter(Role.role_name == role_name, Role.is_deleted == False).first()

def get_roles(db: Session) -> List[Role]:
    return db.query(Role).filter(Role.is_deleted == False).all()

def create_role(db: Session, role_in: RoleCreate) -> Role:
    db_role = Role(
        role_name=role_in.role_name,
        created_by=role_in.created_by
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_in: RoleUpdate) -> Optional[Role]:
    role = get_role(db, role_id)
    if not role:
        return None
    role.role_name = role_in.role_name
    role.modified_by = role_in.modified_by
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int) -> bool:
    role = get_role(db, role_id)
    if not role:
        return False
    role.is_deleted = True
    db.commit()
    return True



def get_all_rolesDD(db: Session) -> List[Dict]:
    try:
        sql = text("SELECT * FROM get_all_roles();")
        result = db.execute(sql)
        rows = result.fetchall()

        # Convert each row to dictionary for JSON serialization
        roles = [
            {
                "role_id": row.role_id,
                "role_name": row.role_name,
                "created_by": row.created_by,
                "created_date": row.created_date,
                "modified_by": row.modified_by,
                "modified_date": row.modified_date,
                "is_deleted": row.is_deleted
            }
            for row in rows
        ]

        return roles
    except Exception as e:
        db.rollback()
        return [{"error": str(e)}]
