from sqlalchemy.orm import Session
from app.models.RolePermissionModel import RolePermission
from app.models.RoleModel import Role
from app.models.MenuModel import Menu, SubMenu
from app.schemas.RolePermissionSchema import RolePermissionsRequestModel
from typing import List


# =====================================================
#  Update Role Permissions
# =====================================================


def save_role_permissions(db: Session, payload: dict):
    user_id = payload["userId"]

    for p in payload["permissions"]:

        # 1️⃣ resolve menu_id from submenu
        submenu = db.query(SubMenu).filter(
            SubMenu.submenu_id == p["subMenuId"]
        ).first()

        if not submenu:
            continue  # invalid submenu → skip

        menu_id = submenu.menu_id

        # 2️⃣ check if permission already exists
        existing = db.query(RolePermission).filter(
            RolePermission.user_id == user_id,
            RolePermission.role_id == p["roleId"],
            RolePermission.submenu_id == p["subMenuId"]
        ).first()

        # 3️⃣ CREATE
        if p["isSelected"] and not existing:
            db.add(
                RolePermission(
                    user_id=user_id,
                    role_id=p["roleId"],
                    menu_id=menu_id,      # ✅ auto derived
                    submenu_id=p["subMenuId"]
                )
            )

        # 4️⃣ DELETE
        elif not p["isSelected"] and existing:
            db.delete(existing)

    db.commit()
    return {"message": "Permissions saved successfully"}


# =====================================================
#  Get Role Permissions
# =====================================================

from sqlalchemy.orm import Session
from sqlalchemy import text



from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.RolePermissionModel import RolePermission
from app.schemas.RolePermissionSchema import RolePermissionsRequestModel


def update_role_permissions_by_rpid(db: Session, payload: dict):
    user_id = payload["userId"]   # ✅ FIXED

    for p in payload["permissions"]:

        # 1️⃣ Existing row
        if p.get("rpId"):

            if p["isSelected"]:
                # UPDATE existing row
                db.query(RolePermission).filter(
                    RolePermission.rp_id == p["rpId"],
                    RolePermission.user_id == user_id
                ).update({
                    RolePermission.role_id: p["roleId"],
                    RolePermission.menu_id: p["menuId"],
                    RolePermission.submenu_id: p["subMenuId"]
                })

            else:
                # DELETE unchecked
                db.query(RolePermission).filter(
                    RolePermission.rp_id == p["rpId"],
                    RolePermission.user_id == user_id
                ).delete()

        # 2️⃣ New permission (rpId is None)
        else:
            if p["isSelected"]:
                db.add(
                    RolePermission(
                        user_id=user_id,
                        role_id=p["roleId"],
                        menu_id=p["menuId"],
                        submenu_id=p["subMenuId"]
                    )
                )

    db.commit()
    return {"message": "Permissions updated successfully"}



# =====================================================
# GET ROLE PERMISSIONS (FOR UI PREFILL)
# =====================================================
from sqlalchemy.orm import Session
from sqlalchemy import text


# def get_role_permissions_by_user(db: Session, user_id: int):
#     rows = db.execute(
#         text("SELECT * FROM get_user_role_permissions_full(:uid)"),
#         {"uid": user_id}
#     ).fetchall()

#     if not rows:
#         return {}

#     user_data = {
#         "user_id": rows[0].user_id,
#         "username": rows[0].username,
#         "first_name": rows[0].first_name,
#         "last_name": rows[0].last_name,
#         "employee_code": rows[0].employee_code,
#         "station_name": rows[0].station_name,
#         "roles": {}
#     }

#     for r in rows:
#         role_id = r.role_id

#         if role_id not in user_data["roles"]:
#             user_data["roles"][role_id] = {
#                 "roleId": r.role_id,
#                 "roleName": r.role_name,
#                 "menus": {}
#             }

#         menus = user_data["roles"][role_id]["menus"]
#         menu_id = r.menu_id

#         if menu_id not in menus:
#             menus[menu_id] = {
#                 "menuId": r.menu_id,
#                 "menuName": r.menu_name,
#                 "subMenus": []
#             }

#         menus[menu_id]["subMenus"].append({
#             "rpId": r.rp_id,
#             "subMenuId": r.submenu_id,
#             "subMenuName": r.submenu_name
#         })

#     # convert nested dict → list
#     user_data["roles"] = [
#         {
#             **role,
#             "menus": list(role["menus"].values())
#         }
#         for role in user_data["roles"].values()
#     ]

#     return user_data


from sqlalchemy import text
from sqlalchemy.orm import Session


def get_all_users_role_permissions(db: Session):
    rows = db.execute(
        text("SELECT * FROM get_all_user_submenu_role_summary()")
    ).fetchall()

    user_map = {}

    for r in rows:
        user_id = r.user_id

        # -------------------------
        # USER LEVEL
        # -------------------------
        # print(r)
        if user_id not in user_map:
            user_map[user_id] = {
                "userId": r.user_id,
                "employeeCode": r.employee_code,
                "is_employee": r.is_employee,
                "employeeName": f"{r.first_name} {r.last_name}",
                "stationName": r.station_name,
                "subModules": {}
            }

        # -------------------------
        # SUBMENU LEVEL
        # -------------------------
        if r.submenu_name:
            user_map[user_id]["subModules"][r.submenu_name] = r.role_name

    return list(user_map.values())


from app.models.UserModel import User


def get_role_permissions_by_user(db: Session, user_id: int):
    # ---------------------------
    # 1️⃣ Fetch user basic info
    # ---------------------------
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        return {
            "message": "User not found"
        }

    # ---------------------------
    # 2️⃣ Fetch permission matrix
    # ---------------------------
    rows = db.execute(
        text("SELECT * FROM get_user_permissions_matrix(:uid)"),
        {"uid": user_id}
    ).fetchall()

    menu_map = {}

    for r in rows:
        menu_id = r.menu_id

        # -------- MENU LEVEL --------
        if menu_id not in menu_map:
            menu_map[menu_id] = {
                "menuId": r.menu_id,
                "menuName": r.menu_name,
                "subMenus": {}
            }

        submenus = menu_map[menu_id]["subMenus"]
        submenu_id = r.submenu_id

        # -------- SUBMENU LEVEL --------
        if submenu_id not in submenus:
            submenus[submenu_id] = {
                "subMenuId": r.submenu_id,
                "subMenuName": r.submenu_name,
                "roles": []
            }

        # -------- ROLE LEVEL --------
        submenus[submenu_id]["roles"].append({
            "roleId": r.role_id,
            "roleName": r.role_name,
            "rpId": r.rp_id,
            "checked": r.checked
        })

    # ---------------------------
    # 3️⃣ Final response
    # ---------------------------
    return {
        "user": {
            "userId": user.user_id,
            "firstName": user.first_name,
            "lastName": user.last_name
        },
        "menus": [
            {
                "menuId": menu["menuId"],
                "menuName": menu["menuName"],
                "subMenus": list(menu["subMenus"].values())
            }
            for menu in menu_map.values()
        ]
    }

