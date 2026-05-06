from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text          # ← correct import
from typing import List
from collections import defaultdict

from app.crud.permit_management.work_height_permit.work_at_height_permit import (
    get_all_work_at_height_permits,
    get_work_at_height_permit_by_id,
    get_work_at_height_permits_by_user_id,
    
)
from app.database import get_db
from app.schemas.permit_management.work_height_permit.work_at_height_permit import (
    WorkAtHeightPermitSchema,
    WorkAtHeightPermitDetailSchema
)

router = APIRouter(
    prefix="/work-at-height-permit",
    tags=["Work At Height Permit"]
)


def get_role_users_directory(db: Session) -> dict:
    """Fetches users mapped to Permit Management (Submenu 4) grouped by role."""
    users_data = (
        db.execute(
            text(
                """
            SELECT rp.user_id, r.role_name
            FROM role_permissions rp
            JOIN roles r ON r.role_id = rp.role_id
            WHERE rp.submenu_id = 4
              AND rp.user_id IS NOT NULL
        """
            )
        )
        .mappings()
        .all()
    )

    users_by_role = defaultdict(list)
    for u in users_data:
        users_by_role[u["role_name"]].append(u["user_id"])

    return {
        "Engineer": users_by_role.get("Engineer", []),
        "EAP": users_by_role.get("EAP", []),
        "SIC": users_by_role.get("SIC", []),
        "ASIC": users_by_role.get("ASIC", []),
        "Admin": users_by_role.get("Admin", []),
    }


# @router.get(
#     "",
#     response_model=List[WorkAtHeightPermitSchema]
# )
# def read_all_work_at_height_permits(
#     db: Session = Depends(get_db)
# ):
#     return get_all_work_at_height_permits(db)


@router.get("/all-permits")
def get_all_permits(db: Session = Depends(get_db)):
    from app.crud.permit_management.work_height_permit.work_at_height_permit import get_all_work_at_height_full

    wah = get_all_work_at_height_full(db)
    role_users = get_role_users_directory(db)

    def sort_key(x):
        val = x.get("updated_at") or x.get("created_at")
        if val is None:
            return ""
        if isinstance(val, str):
            return val
        return val.isoformat()  # convert datetime to string

    wah.sort(key=sort_key, reverse=True)

    for item in wah:
        item["role_users"] = role_users

    return {
        "count": len(wah),
        "data": wah
    }


# ── /user/{user_id} MUST come before /{whp_id} ──────────────
@router.get(
    "/user/{user_id}",
    response_model=List[WorkAtHeightPermitDetailSchema]
)
def read_work_at_height_permits_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_work_at_height_permits_by_user_id(db, user_id)


@router.get(
    "/{whp_id}",
    response_model=WorkAtHeightPermitDetailSchema
)
def read_work_at_height_permit_by_id(
    whp_id: int,
    db: Session = Depends(get_db)
):
    data = get_work_at_height_permit_by_id(db, whp_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Work At Height Permit not found"
        )

    return data


# =================================================
# DELETE
# =================================================
@router.delete("/{whp_id}", summary="Delete Work At Height Permit")
def delete_whp(
    whp_id: int,
    db: Session = Depends(get_db)
):
    # ── Check if record exists and get status ────────────────
    check = db.execute(
        text("SELECT whp_id, status FROM work_at_height_permit WHERE whp_id = :whp_id"),
        {"whp_id": whp_id}
    ).mappings().first()

    if not check:
        raise HTTPException(status_code=404, detail="Work At Height Permit not found")

    if check["status"] != "Draft":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete permit with status '{check['status']}'. Only Draft permits can be deleted."
        )

    # ── Delete child records first ───────────────────────────
    db.execute(text("""
        DELETE FROM work_at_height_toolbox_talk_participant
        WHERE toolbox_talk_id IN (
            SELECT whtt_id FROM work_at_height_toolbox_talk
            WHERE work_at_height_permit_id = :whp_id
        )
    """), {"whp_id": whp_id})

    db.execute(text("""
        DELETE FROM work_at_height_toolbox_talk
        WHERE work_at_height_permit_id = :whp_id
    """), {"whp_id": whp_id})

    db.execute(text("""
        DELETE FROM work_at_height_electrical_isolation_permit
        WHERE whp_id = :whp_id
    """), {"whp_id": whp_id})

    db.execute(text("""
        DELETE FROM work_at_height_electrical_energization_permit
        WHERE whp_id = :whp_id
    """), {"whp_id": whp_id})

    # ── Delete master ────────────────────────────────────────
    db.execute(text("""
        DELETE FROM work_at_height_permit
        WHERE whp_id = :whp_id
    """), {"whp_id": whp_id})

    db.commit()

    return {"message": f"Work At Height Permit {whp_id} deleted successfully"}