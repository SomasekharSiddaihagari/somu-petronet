from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import RolePermissionCrud
from app.routers.UserAuth import get_all_users
from app.schemas.RolePermissionSchema import SaveRolePermissionRequest
from app.utils.UserAuthUtils import verify_access_token

router = APIRouter(prefix="/api", tags=["Role Permissions"])



@router.post("/role-permissions")
def create_role_permissions(
    payload: SaveRolePermissionRequest,
    db: Session = Depends(get_db)
):
    return RolePermissionCrud.save_role_permissions(
        db=db,
        payload=payload.dict()
    )


@router.put("/role-permissions")
def update_role_permissions(
    payload: SaveRolePermissionRequest,
    db: Session = Depends(get_db)
):
    return RolePermissionCrud.save_role_permissions(
        db=db,
        payload=payload.dict()
    )


# @router.get("/get-role-permissions/{user_id}")
# def get_permissions(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return RolePermissionCrud.get_role_permissions_by_user(db, user_id)



@router.get("/get-all-users-role-permissions")
def get_all_role_permissions(db: Session = Depends(get_db)):
    return RolePermissionCrud.get_all_users_role_permissions(db)


@router.get("/get-role-permissions/{user_id}")
def get_permissions(
    user_id: int,
    db: Session = Depends(get_db)
):
    return RolePermissionCrud.get_role_permissions_by_user(db, user_id)

