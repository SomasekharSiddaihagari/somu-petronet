from pydantic import BaseModel
from typing import List, Optional

# ======================================================
# RESPONSE DTOs (GET ROLE PERMISSIONS)
# ======================================================

class SubMenuDto(BaseModel):
    subMenuId: int
    subMenuName: str
    subMenuURL: Optional[str] = None
    subMenuIcon: Optional[str] = None

    class Config:
        from_attributes = True


class MenuDto(BaseModel):
    menuId: int
    menuName: str
    menuURL: Optional[str] = None
    menuIcon: Optional[str] = None
    subMenuLists: List[SubMenuDto]

    class Config:
        from_attributes = True


class RolePermissionViewModel(BaseModel):
    roleId: int
    roleName: str
    getMenuLists: List[MenuDto]

    class Config:
        from_attributes = True


# ======================================================
# REQUEST MODELS (UPDATE / ASSIGN PERMISSIONS)
# ======================================================

class SubMenuPermissionRequest(BaseModel):
    subMenuId: int
    isSelected: bool


class MenuPermissionRequest(BaseModel):
    menuId: int
    subMenuLists: List[SubMenuPermissionRequest]


class RolePermissionRequestModel(BaseModel):
    roleId: int
    menuList: List[MenuPermissionRequest]


class RolePermissionsRequestModel(BaseModel):
    """
    ADMIN assigns permissions to a USER
    """
    userId: int
    rolePermissionsModel: List[RolePermissionRequestModel]


class PermissionItem(BaseModel):
    roleId: int
    subMenuId: int
    isSelected: bool


class UpdateRolePermissionRequest(BaseModel):
    userId: int
    permissions: list[PermissionItem]

class SaveRolePermissionRequest(BaseModel):
    userId: int
    permissions: List[PermissionItem]