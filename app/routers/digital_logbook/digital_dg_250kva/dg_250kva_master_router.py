# app/routers/dg_250kva_router.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.digital_logbook.digital_dg_250kva.dg_250kva_master_schema import (
    DG250KVACreate,
    DG250KVAUpdate
)
from app.crud.digital_logbook.digital_dg_250kva.dg_250kva_master_crud import (
    create_dg_250kva,
    update_dg_250kva,
    delete_dg_250kva
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/dg-250kva",
    tags=["DG 250KVA"],dependencies=[Depends(validate_token)]
)

# @router.get(
#     "/api/logbook/dg-250kva/{ms_logbook_id}",
#     tags=["DG Log Book - 250 KVA"]
# )
# def get_dg_250kva(
#     ms_logbook_id: int,
#     db: Session = Depends(get_db)
# ):
#     # 1️⃣ Fetch shift master
#     shift = db.execute(
#         text("""
#             SELECT *
#             FROM logbook_shift_master
#             WHERE ms_logbook_id = :id
#         """),
#         {"id": ms_logbook_id}
#     ).mappings().first()

#     if not shift:
#         raise HTTPException(
#             status_code=404,
#             detail="Logbook shift master not found"
#         )

#     # 2️⃣ Extract dg_id
#     dg_id = shift["dg_id"]

#     if not dg_id:
#         return {
#             "ms_logbook_id": ms_logbook_id,
#             "module": "dg_250kva",
#             "message": "DG 250 KVA log not created for this shift",
#             "dg_250kva": None
#         }

#     # 3️⃣ Fetch DG master
#     master = db.execute(
#         text("""
#             SELECT *
#             FROM dg_250kva_master
#             WHERE dg_id = :id
#         """),
#         {"id": dg_id}
#     ).mappings().first()

#     if not master:
#         return {
#             "ms_logbook_id": ms_logbook_id,
#             "module": "dg_250kva",
#             "message": "DG 250 KVA master record missing",
#             "dg_250kva": None
#         }

#     # 4️⃣ Fetch DG entries
#     entries = db.execute(
#         text("""
#             SELECT *
#             FROM dg_250kva_entry
#             WHERE master_id = :id
#             ORDER BY log_date, start_time
#         """),
#         {"id": dg_id}
#     ).mappings().all()

#     # 5️⃣ Final response
#     return {
#         "ms_logbook_id": ms_logbook_id,
#         "module": "dg_250kva",
#         "dg_250kva": {
#             "master": master,
#             "entries": entries
#         }
#     }



@router.post("")
def create_dg_250kva_api(
    payload: DG250KVACreate,
    db: Session = Depends(get_db)
):
    dg_id = create_dg_250kva(db, payload)
    return {
        "message": "DG 250KVA master record created successfully",
        "dg_id": dg_id
    }


@router.put("/{dg_id}")
def update_dg_250kva_api(
    dg_id: int,
    payload: DG250KVAUpdate,
    db: Session = Depends(get_db)
):
    updated = update_dg_250kva(db, dg_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "DG 250KVA master record updated successfully"}



# =====================================================
# GET BY DATE
# =====================================================
@router.get("/by-date")
def get_dg_250kva_by_date(
    log_date: date = Query(..., description="e.g. 2026-03-17"),
    station_id: int = Query(..., description="Station ID"),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            m.*,
            s.station_name,
            TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(t.first_name, ''), ' ', COALESCE(t.last_name, ''))) AS technician_full_name
        FROM dg_250kva_master m
        LEFT JOIN users t ON t.user_id = m.technician_id AND t.is_deleted = FALSE
        LEFT JOIN station s ON s.station_id = t.station_id
        LEFT JOIN users u ON u.user_id = m.created_by AND u.is_deleted = FALSE
        WHERE m.entry_date = :log_date
        AND (t.station_id = :station_id OR u.station_id = :station_id)
    """)

    rows = db.execute(query, {
        "log_date": log_date,
        "station_id": station_id
    }).mappings().all()

    if not rows:
        return {"count": 0, "data": []}

    result = []
    for row in rows:
        master_dict = dict(row)
        dg_id = master_dict["dg_id"]

        entries = db.execute(
            text("""
                SELECT
                    e.*,
                    TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                    TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
                FROM dg_250kva_entry e
                LEFT JOIN users uc ON uc.user_id = e.created_by AND uc.is_deleted = FALSE
                LEFT JOIN users uu ON uu.user_id = e.updated_by AND uu.is_deleted = FALSE
                WHERE e.master_id = :dg_id
                ORDER BY e.log_date, e.start_time
            """),
            {"dg_id": dg_id}
        ).mappings().all()

        master_dict["entries"] = [dict(e) for e in entries]
        result.append(master_dict)

    return {"count": len(result), "data": result}



# =====================================================
# GET BY dg_id
# =====================================================
@router.get("/{dg_id}")
def get_dg_250kva_by_id(
    dg_id: int,
    db: Session = Depends(get_db)
):
    master = db.execute(
        text("""
            SELECT
                m.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(t.first_name, ''), ' ', COALESCE(t.last_name, ''))) AS technician_full_name
            FROM dg_250kva_master m
            LEFT JOIN users u ON u.user_id = m.created_by AND u.is_deleted = FALSE
            LEFT JOIN users t ON t.user_id = m.technician_id AND t.is_deleted = FALSE
            WHERE m.dg_id = :dg_id
        """),
        {"dg_id": dg_id}
    ).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail="DG 250KVA master not found")

    entries = db.execute(
        text("""
            SELECT *
            FROM dg_250kva_entry
            WHERE master_id = :dg_id
            ORDER BY log_date, start_time
        """),
        {"dg_id": dg_id}
    ).mappings().all()

    return {
        "data": {
            **dict(master),
            "entries": [dict(e) for e in entries]
        }
    }


@router.delete("/{dg_id}")
def delete_dg_250kva_api(
    dg_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_dg_250kva(db, dg_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="DG 250KVA master record not found"
        )

    return {"message": "DG 250KVA master record deleted successfully"}
