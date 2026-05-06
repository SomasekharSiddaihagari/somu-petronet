from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List
from collections import defaultdict

from app.crud.permit_management.composit_permit.composite_work_permit import (
    get_all_cwp,
    get_cwp_by_id,
    get_cwp_by_user_id,
    get_all_cwp_full
)
from app.database import get_db
from app.schemas.permit_management.composit_permit.composite_work_permit import (
    CompositeWorkPermitSchema,
    CompositeWorkPermitDetailSchema
)

router = APIRouter(
    prefix="/composite-work-permit",
    tags=["Composite Work Permit"]
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
#     response_model=List[CompositeWorkPermitSchema]
# )
# def read_all_composite_work_permits(
#     db: Session = Depends(get_db)
# ):
#     return get_all_cwp(db)



@router.get("/all-permits")
def get_all_permits(db: Session = Depends(get_db)):

    cwp_data = get_all_cwp_full(db)
    role_users = get_role_users_directory(db)

    for item in cwp_data:
        item["role_users"] = role_users

    return {
        "count": len(cwp_data),
        "data": cwp_data
    }


# ── /user/{user_id} MUST come before /{cwp_id} ──────────────
@router.get(
    "/user/{user_id}",
    response_model=List[CompositeWorkPermitDetailSchema]
)
def read_composite_work_permits_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_cwp_by_user_id(db, user_id)


@router.get(
    "/{cwp_id}",
    response_model=CompositeWorkPermitDetailSchema
)
def read_composite_work_permit_by_id(
    cwp_id: int,
    db: Session = Depends(get_db)
):
    data = get_cwp_by_id(db, cwp_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Composite Work Permit not found"
        )

    return data


# =================================================
# DELETE
# =================================================
@router.delete("/{cwp_id}", summary="Delete Composite Work Permit")
def delete_cwp(
    cwp_id: int,
    db: Session = Depends(get_db)
):
    # ── Check if record exists and get status ────────────────
    check = db.execute(
        text("SELECT cwp_id, status FROM composite_work_permit WHERE cwp_id = :cwp_id"),
        {"cwp_id": cwp_id}
    ).mappings().first()

    if not check:
        raise HTTPException(status_code=404, detail="Composite Work Permit not found")

    if check["status"] != "Draft":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete permit with status '{check['status']}'. Only Draft permits can be deleted."
        )

    # ── Delete child records first ───────────────────────────

    # participants → toolbox talks → isolation → energization → master
    db.execute(text("""
        DELETE FROM composite_toolbox_talk_participant
        WHERE toolbox_talk_id IN (
            SELECT ctt_id FROM composite_toolbox_talk
            WHERE composite_work_permit_id = :cwp_id
        )
    """), {"cwp_id": cwp_id})

    db.execute(text("""
        DELETE FROM composite_toolbox_talk
        WHERE composite_work_permit_id = :cwp_id
    """), {"cwp_id": cwp_id})

    db.execute(text("""
        DELETE FROM composite_electrical_isolation_permit
        WHERE composite_work_permit_id = :cwp_id
    """), {"cwp_id": cwp_id})

    db.execute(text("""
        DELETE FROM composite_electrical_energization_permit
        WHERE composite_work_permit_id = :cwp_id
    """), {"cwp_id": cwp_id})

    # ── Delete master ────────────────────────────────────────
    db.execute(text("""
        DELETE FROM composite_work_permit
        WHERE cwp_id = :cwp_id
    """), {"cwp_id": cwp_id})

    db.commit()

    return {"message": f"Composite Work Permit {cwp_id} deleted successfully"}