# app/routers/dg_250kva_entry_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.digital_logbook.digital_dg_250kva.dg_250kva_entry_schema import (
    DG250KVAEntryCreate,
    DG250KVAEntryUpdate
)
from app.crud.digital_logbook.digital_dg_250kva.dg_250kva_entry_crud import (
    create_dg_250kva_entry,
    update_dg_250kva_entry,
    delete_dg_250kva_entry
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/dg-250kva-entry",
    tags=["DG 250KVA Entry"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_dg_250kva_entry_api(
    payload: DG250KVAEntryCreate,
    db: Session = Depends(get_db)
):
    entry_id = create_dg_250kva_entry(db, payload)
    return {
        "message": "DG 250KVA entry created successfully",
        "dg_entry_id": entry_id
    }


@router.put("/{dg_entry_id}")
def update_dg_250kva_entry_api(
    dg_entry_id: int,
    payload: DG250KVAEntryUpdate,
    db: Session = Depends(get_db)
):
    updated = update_dg_250kva_entry(db, dg_entry_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "DG 250KVA entry updated successfully"}


@router.get("/{dg_entry_id}")
def get_dg_250kva_entry_by_id(
    dg_entry_id: int,
    db: Session = Depends(get_db)
):
    entry = db.execute(
        text("""
            SELECT
                e.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name
            FROM dg_250kva_entry e
            LEFT JOIN users u ON u.user_id = e.created_by AND u.is_deleted = FALSE
            WHERE e.dg_entry_id = :dg_entry_id
        """),
        {"dg_entry_id": dg_entry_id}
    ).mappings().first()

    if not entry:
        raise HTTPException(status_code=404, detail="DG 250KVA entry not found")

    return {"data": dict(entry)}


@router.delete("/{dg_entry_id}")
def delete_dg_250kva_entry_api(
    dg_entry_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_dg_250kva_entry(db, dg_entry_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="DG 250KVA entry not found"
        )

    return {"message": "DG 250KVA entry deleted successfully"}
