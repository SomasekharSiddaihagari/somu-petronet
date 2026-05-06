from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.crud.digital_logbook.digital_logbook_linewalker.line_walker_master_crud import create_line_walker_master, delete_line_walker_master, update_line_walker_master
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_linewalker.line_walker_master_schemas import LineWalkerMasterCreate, LineWalkerMasterUpdate
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/line-walker-master",
    tags=["Line Walker Master"],dependencies=[Depends(validate_token)]
)

# @router.get("/line-walker/{ms_logbook_id}")
# def get_line_walker_log(
#     ms_logbook_id: int,
#     db: Session = Depends(get_db)
# ):
#     # 1️⃣ Fetch shift master
#     shift_sql = text("""
#         SELECT *
#         FROM logbook_shift_master
#         WHERE ms_logbook_id = :ms_logbook_id
#     """)

#     shift = db.execute(
#         shift_sql,
#         {"ms_logbook_id": ms_logbook_id}
#     ).mappings().first()

#     if not shift:
#         raise HTTPException(
#             status_code=404,
#             detail="Logbook shift master not found"
#         )

#     # 2️⃣ Extract line_walker_id
#     line_walker_id = shift["line_walker_id"]

#     if not line_walker_id:
#         return {
#             "ms_logbook_id": ms_logbook_id,
#             "module": "line_walker",
#             "message": "Line Walker report not created for this shift",
#             "line_walker": None
#         }

#     # 3️⃣ Fetch Line Walker master
#     master_sql = text("""
#         SELECT *
#         FROM line_walker_master
#         WHERE line_walker_id = :line_walker_id
#     """)

#     master = db.execute(
#         master_sql,
#         {"line_walker_id": line_walker_id}
#     ).mappings().first()

#     if not master:
#         return {
#             "ms_logbook_id": ms_logbook_id,
#             "module": "line_walker",
#             "message": "Line Walker master record missing",
#             "line_walker": None
#         }

#     # 4️⃣ Fetch Line Walker entries
#     entry_sql = text("""
#         SELECT *
#         FROM line_walker_entry
#         WHERE line_walker_id = :line_walker_id
#         ORDER BY start_time
#     """)

#     entries = db.execute(
#         entry_sql,
#         {"line_walker_id": line_walker_id}
#     ).mappings().all()

#     # 5️⃣ Fetch Supervisor entries
#     supervisor_sql = text("""
#         SELECT *
#         FROM supervisor_entry
#         WHERE line_walker_id = :line_walker_id
#         ORDER BY sl_no
#     """)

#     supervisors = db.execute(
#         supervisor_sql,
#         {"line_walker_id": line_walker_id}
#     ).mappings().all()

#     # 6️⃣ Final response
#     return {
#         "ms_logbook_id": ms_logbook_id,
#         "module": "line_walker",
#         "line_walker": {
#             "master": master,
#             "walker_entries": entries,
#             "supervisor_entries": supervisors
#         }
#     }

# =====================================================
# POST — CREATE
# =====================================================

@router.post("")
def create_master(
    payload: LineWalkerMasterCreate,
    db: Session = Depends(get_db)
):
    data = {k: v for k, v in payload.dict().items() if v is not None}
    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data])

    result = db.execute(
        text(f"""
            INSERT INTO line_walker_master ({cols})
            VALUES ({vals})
            RETURNING line_walker_id
        """),
        data
    )
    db.commit()

    return {"line_walker_id": result.fetchone()[0]}




@router.get("/by-date")
def get_line_walker_master_by_date(
    log_date: date,
    station_id: int = Query(..., description="Station ID"),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            lwm.*,
            TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
            CASE
                WHEN LSM.ms_logbook_id IS NOT NULL AND EXTRACT(HOUR FROM LSM.created_at) < 7
                THEN DATE(LSM.created_at - INTERVAL '1 day')
                WHEN LSM.ms_logbook_id IS NOT NULL
                THEN DATE(LSM.created_at)
                ELSE DATE(lwm.created_at)
            END AS logbook_date
        FROM line_walker_master lwm
        LEFT JOIN users u
            ON u.user_id = lwm.created_by
            AND u.is_deleted = FALSE
        LEFT JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = lwm.ms_logbook_id
        WHERE
            CASE
                WHEN LSM.ms_logbook_id IS NOT NULL AND EXTRACT(HOUR FROM LSM.created_at) < 7
                THEN DATE(LSM.created_at - INTERVAL '1 day')
                WHEN LSM.ms_logbook_id IS NOT NULL
                THEN DATE(LSM.created_at)
                ELSE DATE(lwm.created_at)
            END = :log_date
          AND u.station_id = :station_id
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
        line_walker_id = master_dict["line_walker_id"]

        # ✅ walker entries with created_by_name
        entries = db.execute(
            text("""
                SELECT
                    lwe.*,
                    TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                    TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
                FROM line_walker_entry lwe
                LEFT JOIN users uc ON uc.user_id = lwe.created_by AND uc.is_deleted = FALSE
                LEFT JOIN users uu ON uu.user_id = lwe.updated_by AND uu.is_deleted = FALSE
                WHERE lwe.line_walker_id = :line_walker_id
                ORDER BY lwe.start_time
            """),
            {"line_walker_id": line_walker_id}
        ).mappings().all()

        # ✅ supervisor entries with created_by_name
        supervisors = db.execute(
            text("""
                SELECT
                    se.*,
                    TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                    TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
                FROM supervisor_entry se
                LEFT JOIN users uc ON uc.user_id = se.created_by AND uc.is_deleted = FALSE
                LEFT JOIN users uu ON uu.user_id = se.updated_by AND uu.is_deleted = FALSE
                WHERE se.line_walker_id = :line_walker_id
                ORDER BY se.sl_no
            """),
            {"line_walker_id": line_walker_id}
        ).mappings().all()

        master_dict["walker_entries"] = [dict(e) for e in entries]
        master_dict["supervisor_entries"] = [dict(s) for s in supervisors]
        result.append(master_dict)

    return {"count": len(result), "data": result}



# =====================================================
# GET BY ID
# =====================================================

@router.get("/{line_walker_id}")
def get_line_walker_master_by_id(
    line_walker_id: int,
    db: Session = Depends(get_db)
):
    master = db.execute(
        text("""
            SELECT
                lwm.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name
            FROM line_walker_master lwm
            LEFT JOIN users u
                ON u.user_id = lwm.created_by
                AND u.is_deleted = FALSE
            WHERE lwm.line_walker_id = :line_walker_id
        """),
        {"line_walker_id": line_walker_id}
    ).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail="Line Walker master not found")

    entries = db.execute(
        text("""
            SELECT *
            FROM line_walker_entry
            WHERE line_walker_id = :line_walker_id
            ORDER BY start_time
        """),
        {"line_walker_id": line_walker_id}
    ).mappings().all()

    supervisors = db.execute(
        text("""
            SELECT *
            FROM supervisor_entry
            WHERE line_walker_id = :line_walker_id
            ORDER BY sl_no
        """),
        {"line_walker_id": line_walker_id}
    ).mappings().all()

    data = dict(master)
    data["walker_entries"] = [dict(e) for e in entries]
    data["supervisor_entries"] = [dict(s) for s in supervisors]

    return {"data": data}


# =====================================================
# PUT — UPDATE
# =====================================================

@router.put("/{line_walker_id}")
def update_master(
    line_walker_id: int,
    payload: LineWalkerMasterUpdate,
    db: Session = Depends(get_db)
):
    data = {k: v for k, v in payload.dict().items() if v is not None}

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    sets = ", ".join([f"{k} = :{k}" for k in data])
    data["line_walker_id"] = line_walker_id

    result = db.execute(
        text(f"""
            UPDATE line_walker_master
            SET {sets}
            WHERE line_walker_id = :line_walker_id
        """),
        data
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Line Walker master not found")

    return {"message": "Updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{line_walker_id}")
def delete_master(
    line_walker_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM line_walker_master
            WHERE line_walker_id = :id
        """),
        {"id": line_walker_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Line Walker master not found")

    return {"message": "Deleted successfully"}
