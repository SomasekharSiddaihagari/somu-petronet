from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from typing import List

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/tank-dip-memo",
    tags=["Tank Dip Memo"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class TankDipMemoCreate(BaseModel):
    # Header
    document_no: Optional[str]
    station_name: Optional[str]
    station_incharge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    status: Optional[str]

    # Tank details
    tank_no: Optional[str]
    company: Optional[str]
    product: Optional[str]
    memo_no: Optional[str]

    mrpl_batch_no: Optional[str]
    pmhbl_batch_no: Optional[str]

    before_after_mrpl: Optional[str]   # Before / After / Received
    before_after_mrpl_qty: Optional[str] = None

    # Date & Time
    dip_time: Optional[time]
    dip_date: Optional[date]

    # DIP Measurements
    ref_height_cm: Optional[float]
    ullage_at_natural: Optional[float]
    gross_dip_cm: Optional[float]
    dip_of_water_mm: Optional[float]

    # Temperature
    temp_top: Optional[float]
    temp_middle: Optional[float]
    temp_bottom: Optional[float]
    temp_average: Optional[float]
    tank_temp: Optional[float]

    # Density
    density_top: Optional[float]
    density_middle: Optional[float]
    density_bottom: Optional[float]
    density_average: Optional[float]
    density_tank: Optional[float]

    density_at_15c: Optional[float]

    # Settling Time
    settling_time_pmhbl: Optional[str]
    settling_time_hpcl: Optional[str]
    settling_time_bpcl_iocl: Optional[str]
    settling_time_mrpl: Optional[str]

    # Footer
    entered_by_name: Optional[str]
    entered_date: Optional[date]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    ms_logbook_id: Optional[int] = None
    


class TankDipMemoUpdate(TankDipMemoCreate):
    pass


# =====================================================
# POST — CREATE
# =====================================================
@router.post("")
def create_tank_dip_memo(
    payload: TankDipMemoCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO tank_dip_memo (
            document_no,
            station_name,
            station_incharge,
            shift,
            start_time,
            status,

            tank_no,
            company,
            product,
            memo_no,

            mrpl_batch_no,
            pmhbl_batch_no,
            before_after_mrpl,
            before_after_mrpl_qty,

            dip_time,
            dip_date,

            ref_height_cm,
            ullage_at_natural,
            gross_dip_cm,
            dip_of_water_mm,

            temp_top,
            temp_middle,
            temp_bottom,
            temp_average,
            tank_temp,

            density_top,
            density_middle,
            density_bottom,
            density_average,
            density_tank,
            density_at_15c,

            settling_time_pmhbl,
            settling_time_hpcl,
            settling_time_bpcl_iocl,
            settling_time_mrpl,

            entered_by_name,
            entered_date   ,created_at,created_by ,updated_at ,updated_by, ms_logbook_id

        )
        VALUES (
            :document_no,
            :station_name,
            :station_incharge,
            :shift,
            :start_time,
            :status,

            :tank_no,
            :company,
            :product,
            :memo_no,

            :mrpl_batch_no,
            :pmhbl_batch_no,
            :before_after_mrpl,
            :before_after_mrpl_qty,

            :dip_time,
            :dip_date,

            :ref_height_cm,
            :ullage_at_natural,
            :gross_dip_cm,
            :dip_of_water_mm,

            :temp_top,
            :temp_middle,
            :temp_bottom,
            :temp_average,
            :tank_temp,

            :density_top,
            :density_middle,
            :density_bottom,
            :density_average,
            :density_tank,
            :density_at_15c,

            :settling_time_pmhbl,
            :settling_time_hpcl,
            :settling_time_bpcl_iocl,
            :settling_time_mrpl,

            :entered_by_name,
            :entered_date,:created_at,:created_by ,:updated_at ,:updated_by,:ms_logbook_id

        )
        RETURNING tank_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Tank dip memo created successfully",
        "tank_id": result.scalar()
    }



@router.get("/tank-dip/{ms_logbook_id}")
def get_tank_dip_memo(
    ms_logbook_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch shift master
    shift_sql = text("""
        SELECT *
        FROM logbook_shift_master
        WHERE ms_logbook_id = :ms_logbook_id
    """)

    shift = db.execute(
        shift_sql,
        {"ms_logbook_id": ms_logbook_id}
    ).mappings().first()

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Logbook shift master not found"
        )

    # 2️⃣ Extract tank_id
    tank_id = shift["tank_id"]

    if not tank_id:
        return {
            "ms_logbook_id": ms_logbook_id,
            "module": "tank_dip_memo",
            "message": "Tank DIP Memo not created for this shift",
            "tank_dip_memo": None
        }

    # 3️⃣ Fetch Tank DIP Memo
    memo_sql = text("""
        SELECT *
        FROM tank_dip_memo
        WHERE tank_id = :tank_id
    """)

    memo = db.execute(
        memo_sql,
        {"tank_id": tank_id}
    ).mappings().first()

    if not memo:
        return {
            "ms_logbook_id": ms_logbook_id,
            "module": "tank_dip_memo",
            "message": "Tank DIP Memo record missing",
            "tank_dip_memo": None
        }

    # 4️⃣ Final response
    return {
        "ms_logbook_id": ms_logbook_id,
        "module": "tank_dip_memo",
        "tank_dip_memo": memo
    }



# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{tank_id}")
def update_tank_dip_memo(
    tank_id: int,
    payload: TankDipMemoUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = tank_id

    query = text("""
        UPDATE tank_dip_memo
        SET
            document_no = :document_no,
            station_name = :station_name,
            station_incharge = :station_incharge,
            shift = :shift,
            start_time = :start_time,
            status = :status,

            tank_no = :tank_no,
            company = :company,
            product = :product,
            memo_no = :memo_no,

            mrpl_batch_no = :mrpl_batch_no,
            pmhbl_batch_no = :pmhbl_batch_no,
            before_after_mrpl = :before_after_mrpl,
            before_after_mrpl_qty=:before_after_mrpl_qty,

            dip_time = :dip_time,
            dip_date = :dip_date,

            ref_height_cm = :ref_height_cm,
            ullage_at_natural = :ullage_at_natural,
            gross_dip_cm = :gross_dip_cm,
            dip_of_water_mm = :dip_of_water_mm,

            temp_top = :temp_top,
            temp_middle = :temp_middle,
            temp_bottom = :temp_bottom,
            temp_average = :temp_average,
            tank_temp = :tank_temp,

            density_top = :density_top,
            density_middle = :density_middle,
            density_bottom = :density_bottom,
            density_average = :density_average,
            density_tank = :density_tank,
            density_at_15c = :density_at_15c,

            settling_time_pmhbl = :settling_time_pmhbl,
            settling_time_hpcl = :settling_time_hpcl,
            settling_time_bpcl_iocl = :settling_time_bpcl_iocl,
            settling_time_mrpl = :settling_time_mrpl

            entered_by_name = :entered_by_name,
            entered_date = :entered_date ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by,ms_logbook_id=:ms_logbook_id

        WHERE tank_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Tank dip memo not found"
        )

    return {"message": "Tank dip memo updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{tank_id}")
def delete_tank_dip_memo(
    tank_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM tank_dip_memo
            WHERE tank_id = :id
        """),
        {"id": tank_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Tank dip memo not found"
        )

    return {"message": "Tank dip memo deleted successfully"}

@router.get("/by-date", response_model=List[dict])
def fetch_tank_dip_by_date(
    log_date: date,
    station_name: str,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT TDM.*
        FROM tank_dip_memo TDM
        JOIN logbook_shift_master LSM 
            ON LSM.ms_logbook_id = TDM.ms_logbook_id
        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        AND TDM.station_name = :station_name 
    """)

    result = db.execute(
        query,
        {
            "log_date": log_date,
            "station_name": station_name
        }
    ).mappings().all()

    return result


@router.get("/{tank_id}", response_model=dict)
def fetch_tank_dip_by_id(
    tank_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT *
        FROM tank_dip_memo 
        WHERE tank_id = :tank_id
    """)

    result = db.execute(
        query, {"tank_id": tank_id}
    ).mappings().first()

    return result
