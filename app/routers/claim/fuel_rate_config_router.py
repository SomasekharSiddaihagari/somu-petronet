from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.schemas.claim.fuel_rate_config_schema import (
    FuelRateCreate,
    FuelRateUpdate,
    FuelRateResponse
)

router = APIRouter(
    prefix="/fuel-rate",
    tags=["Fuel Rate Config"]
)


@router.get("/fuel-rate-config")
def get_all_fuel_rates(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                fuel_claim_id,
                petrol_rate,
                others_rate,
                created_at,
                updated_at
            FROM fuel_rate_config
            ORDER BY fuel_claim_id DESC
        """)

        result = db.execute(query)
        rows = result.fetchall()

        if not rows:
            return {"message": "No fuel rate records found", "data": []}

        data = []
        for row in rows:
            data.append({
                "fuel_claim_id": row.fuel_claim_id,
                "petrol_rate": row.petrol_rate,
                "others_rate": row.others_rate,
                "created_at": row.created_at,
                "updated_at": row.updated_at
            })

        return {
            "message": "Fuel rate records fetched successfully",
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/create", response_model=FuelRateResponse)
def create_fuel_rate(payload: FuelRateCreate, db: Session = Depends(get_db)):

    insert_query = text("""
        INSERT INTO fuel_rate_config (petrol_rate, others_rate)
        VALUES (:petrol_rate, :others_rate)
        RETURNING fuel_claim_id, petrol_rate, others_rate, created_at, updated_at
    """)

    result = db.execute(insert_query, payload.dict()).fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="Failed to create fuel rate")

    history_query = text("""
        INSERT INTO fuel_rate_config_history
        (fuel_claim_id, petrol_rate, others_rate)
        VALUES (:fuel_claim_id, :petrol_rate, :others_rate)
    """)

    db.execute(history_query, {
        "fuel_claim_id": result.fuel_claim_id,
        "petrol_rate": result.petrol_rate,
        "others_rate": result.others_rate
    })

    db.commit()
    return dict(result._mapping)


@router.get("/latest", response_model=FuelRateResponse)
def get_latest_fuel_rate(db: Session = Depends(get_db)):

    query = text("""
        SELECT fuel_claim_id, petrol_rate, others_rate, created_at, updated_at
        FROM fuel_rate_config
        ORDER BY fuel_claim_id DESC
        LIMIT 1
    """)

    result = db.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Fuel rate config not found")

    return dict(result._mapping)


@router.get("/{rate_id}", response_model=FuelRateResponse)
def get_fuel_rate(rate_id: int, db: Session = Depends(get_db)):

    query = text("""
        SELECT fuel_claim_id, petrol_rate, others_rate, created_at, updated_at
        FROM fuel_rate_config
        WHERE fuel_claim_id = :rate_id
    """)

    result = db.execute(query, {"rate_id": rate_id}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Fuel rate config not found")

    return dict(result._mapping)


@router.put("/{rate_id}", response_model=FuelRateResponse)
def update_fuel_rate(
    rate_id: int,
    payload: FuelRateUpdate,
    db: Session = Depends(get_db)
):
    update_data = payload.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join([f"{k} = :{k}" for k in update_data.keys()])
    update_data["rate_id"] = rate_id

    update_query = text(f"""
        UPDATE fuel_rate_config
        SET {set_clause}, updated_at = NOW()
        WHERE fuel_claim_id = :rate_id
        RETURNING fuel_claim_id, petrol_rate, others_rate, created_at, updated_at
    """)

    result = db.execute(update_query, update_data).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Fuel rate config not found")

    history_query = text("""
        INSERT INTO fuel_rate_config_history
        (fuel_claim_id, petrol_rate, others_rate)
        VALUES (:fuel_claim_id, :petrol_rate, :others_rate)
    """)

    db.execute(history_query, {
        "fuel_claim_id": result.fuel_claim_id,
        "petrol_rate": result.petrol_rate,
        "others_rate": result.others_rate
    })

    db.commit()
    return dict(result._mapping)


@router.delete("/{rate_id}")
def delete_fuel_rate(rate_id: int, db: Session = Depends(get_db)):

    query = text("""
        DELETE FROM fuel_rate_config
        WHERE fuel_claim_id = :rate_id
        RETURNING fuel_claim_id
    """)

    result = db.execute(query, {"rate_id": rate_id}).fetchone()
    db.commit()

    if not result:
        raise HTTPException(status_code=404, detail="Fuel rate config not found")

    return {"message": "Fuel rate config deleted successfully"}





