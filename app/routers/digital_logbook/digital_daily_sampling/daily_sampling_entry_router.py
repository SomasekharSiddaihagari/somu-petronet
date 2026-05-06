from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/daily-sampling-entry",
    tags=["Daily Sampling Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class DailySamplingEntryCreate(BaseModel):
    master_id: Optional[int]
    sr_no: Optional[int]
    date: Optional[date]
    sample_time: Optional[time]

    product: Optional[str]
    batch_no: Optional[str]
    tank: Optional[str]
    position: Optional[str]
    appearance: Optional[str]
    colour: Optional[str]
    temperature: Optional[str]
    density: Optional[str]
    kinematic_viscosity: Optional[str]
    density_at_15c: Optional[str]
    qc_density: Optional[str]
    difference: Optional[str]

    drawn_by: Optional[str]
    reason_for_sample_testing: Optional[str]

    disposal_date: Optional[date] # type: ignore
    disposed_by: Optional[str]
    org_sign: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class DailySamplingEntryUpdate(DailySamplingEntryCreate):
    pass


# =====================================================
# POST API – CREATE ENTRY

@router.post("")
def create_daily_sampling_entry(
    payload: DailySamplingEntryCreate,
    db: Session = Depends(get_db)
    ):
    query = text("""
        INSERT INTO daily_sampling_entry (
            master_id, sr_no, date, sample_time,

            product, batch_no, tank, position, appearance, colour,
            density, kinematic_viscosity, density_at_15c, qc_density, difference,
            drawn_by, reason_for_sample_testing,
            disposal_date, disposed_by, org_sign
       
                    ,created_at,created_by ,updated_at ,updated_by,temperature
 )
        VALUES (
            :master_id, :sr_no, :date, :sample_time,

            :product, :batch_no, :tank, :position, :appearance, :colour,
            :density, :kinematic_viscosity, :density_at_15c, :qc_density, :difference,
            :drawn_by, :reason_for_sample_testing,
            :disposal_date, :disposed_by, :org_sign
        ,:created_at,:created_by ,:updated_at ,:updated_by,:temperature

                 )
        RETURNING sampling_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Daily Sampling Entry created successfully",
        "sampling_entry_id": result.scalar()
    }


# @router.get("/daily-sampling/entry/{sampling_entry_id}")
# def get_daily_sampling_entry(
#     sampling_entry_id: int,
#     db: Session = Depends(get_db)
#     ):
#     # 1️⃣ Fetch single entry by entry_id
#     entry_sql = text("""
#         SELECT *
#         FROM daily_sampling_entry
#         WHERE sampling_entry_id = :sampling_entry_id
#     """)

#     entry = db.execute(
#         entry_sql,
#         {"sampling_entry_id": sampling_entry_id}
#     ).mappings().first()

#     if not entry:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Daily Sampling entry with id {sampling_entry_id} not found"
#         )

#     # 2️⃣ Fetch its master record
#     master_sql = text("""
#         SELECT *
#         FROM daily_sampling_master
#         WHERE sampling_id = :master_id
#     """)

#     master = db.execute(
#         master_sql,
#         {"master_id": entry["master_id"]}
#     ).mappings().first()

#     # 3️⃣ Final response
#     return {
#         "module": "daily_sampling",
#         "daily_sampling": {
#             "master": dict(master) if master else None,
#             "entry": dict(entry)
#         }
#     }
@router.get("/daily-sampling/entry/{sampling_entry_id}")
def get_daily_sampling_entry(
    sampling_entry_id: int,
    db: Session = Depends(get_db)
    ):
    # 1️⃣ Fetch single entry by entry_id with creator/updater names
    entry_sql = text("""
        SELECT 
            dse.*,
            CONCAT(uc.first_name, ' ', uc.last_name) AS created_by_name,
            CONCAT(uu.first_name, ' ', uu.last_name) AS updated_by_name
        FROM daily_sampling_entry dse
        LEFT JOIN users uc ON uc.user_id = dse.created_by
        LEFT JOIN users uu ON uu.user_id = dse.updated_by
        WHERE dse.sampling_entry_id = :sampling_entry_id
    """)

    entry = db.execute(
        entry_sql,
        {"sampling_entry_id": sampling_entry_id}
    ).mappings().first()

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"Daily Sampling entry with id {sampling_entry_id} not found"
        )

    # 2️⃣ Fetch its master record with creator/updater names
    master_sql = text("""
        SELECT 
            dsm.*,
            CONCAT(uc.first_name, ' ', uc.last_name) AS created_by_name,
            CONCAT(uu.first_name, ' ', uu.last_name) AS updated_by_name
        FROM daily_sampling_master dsm
        LEFT JOIN users uc ON uc.user_id = dsm.created_by
        LEFT JOIN users uu ON uu.user_id = dsm.updated_by
        WHERE dsm.sampling_id = :master_id
    """)

    master = db.execute(
        master_sql,
        {"master_id": entry["master_id"]}
    ).mappings().first()

    # 3️⃣ Final response
    return {
        "module": "daily_sampling",
        "daily_sampling": {
            "master": dict(master) if master else None,
            "entry": dict(entry)
        }
    }



# =====================================================
# PUT API – UPDATE ENTRY
# =====================================================

@router.put("/{entry_id}")
def update_daily_sampling_entry(
    entry_id: int,
    payload: DailySamplingEntryUpdate,
    db: Session = Depends(get_db)
    ):
    query = text("""
        UPDATE daily_sampling_entry
        SET
            master_id = :master_id,
            sr_no = :sr_no,
            date = :date,
            sample_time = :sample_time,

            product = :product,
            batch_no = :batch_no,
            tank = :tank,
            position = :position,
            appearance = :appearance,
            colour = :colour,
            temperature = :temperature,
            density = :density,
            kinematic_viscosity = :kinematic_viscosity,
            density_at_15c = :density_at_15c,
            qc_density = :qc_density,
            difference = :difference,

            drawn_by = :drawn_by,
            reason_for_sample_testing = :reason_for_sample_testing,

            disposal_date = :disposal_date,
            disposed_by = :disposed_by,
            org_sign = :org_sign
                             ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE sampling_entry_id = :entry_id
    """)

    params = payload.dict()
    params["entry_id"] = entry_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Daily sampling entry not found")

    return {"message": "Daily Sampling Entry updated successfully"}


# =====================================================
# DELETE API – DELETE ENTRY
# =====================================================

@router.delete("/{entry_id}")
def delete_daily_sampling_entry(
    entry_id: int,
    db: Session = Depends(get_db)
    ):
    query = text("""
        DELETE FROM daily_sampling_entry
        WHERE sampling_entry_id = :entry_id
    """)

    result = db.execute(query, {"entry_id": entry_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Daily sampling entry not found")

    return {"message": "Daily Sampling Entry deleted successfully"}
