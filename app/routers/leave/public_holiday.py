from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import date
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.UserAuthUtils import verify_access_token   # adjust path if needed

router = APIRouter(prefix="/api/holidays", tags=["Public Holidays/ RH Holiday"])


# -------------------------------------------------------------
# Pydantic Schemas (Compatible with Pydantic V2)
# -------------------------------------------------------------
class HolidayCreate(BaseModel):
    holiday_name: str | None = None
    holiday_type: str | None = None
    holiday_date: date | None = None
    status: str | None = None


class HolidayUpdate(BaseModel):
    holiday_name: str | None = None
    holiday_type: str | None = None
    holiday_date: date | None = None
    status: str | None = None


# -------------------------------------------------------------
# 6) GET — All Holidays 
# -------------------------------------------------------------
@router.get("/all", response_model=None)
def get_holiday_by_type( db: Session = Depends(get_db)):
    query = """
        SELECT *
        FROM hr_public_holiday
        ORDER BY holiday_date ASC;
    """

    rows = db.execute(text(query), ).fetchall()
    return [dict(r._mapping) for r in rows]


# -------------------------------------------------------------
# 1) POST — Create Holiday
# -------------------------------------------------------------
@router.post("/holiday", response_model=None)
def create_holiday(data: HolidayCreate, db: Session = Depends(get_db),  current_user: str = Depends(verify_access_token)
):
    if not current_user:
                    raise HTTPException(status_code=401, detail="Unauthorized user.")

    query = """
        INSERT INTO hr_public_holiday 
            (holiday_name, holiday_type, holiday_date, status)
        VALUES 
            (:holiday_name, :holiday_type, :holiday_date, :status)
        RETURNING public_holiday_id;
    """

    result = db.execute(text(query), data.model_dump())
    new_id = result.scalar()
    db.commit()

    return {"message": "Holiday created", "id": new_id}


# -------------------------------------------------------------
# 2) PUT — Update Holiday
# -------------------------------------------------------------
@router.put("/{holiday_id}", response_model=None)
def update_holiday(holiday_id: int, data: HolidayUpdate, db: Session = Depends(get_db)):
    params = data.model_dump()
    params["holiday_id"] = holiday_id

    query = """
        UPDATE hr_public_holiday
        SET 
            holiday_name = :holiday_name,
            holiday_type = :holiday_type,
            holiday_date = :holiday_date,
            status = :status,
            updated_at = NOW()
        WHERE public_holiday_id = :holiday_id;
    """

    result = db.execute(text(query), params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Holiday not found")

    return {"message": "Holiday updated"}


# -------------------------------------------------------------
# 3) DELETE — Remove Holiday
# -------------------------------------------------------------
@router.delete("/{holiday_id}", response_model=None)
def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    query = """
        DELETE FROM hr_public_holiday
        WHERE public_holiday_id = :holiday_id;
    """

    result = db.execute(text(query), {"holiday_id": holiday_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Holiday not found")

    return {"message": "Holiday deleted"}


# -------------------------------------------------------------
# 4) GET — All Holidays by Type
# -------------------------------------------------------------
@router.get("/type/{holiday_type}", response_model=None)
def get_holiday_by_type(holiday_type: str, db: Session = Depends(get_db)):
    query = """
        SELECT *
        FROM hr_public_holiday
        WHERE holiday_type = :holiday_type;
    """

    rows = db.execute(text(query), {"holiday_type": holiday_type}).fetchall()
    return [dict(r._mapping) for r in rows]


# -------------------------------------------------------------
# 5) GET — Holiday by ID
# -------------------------------------------------------------
@router.get("/{holiday_id}", response_model=None)
def get_holiday_by_id(holiday_id: int, db: Session = Depends(get_db)):
    query = """
        SELECT *
        FROM hr_public_holiday
        WHERE public_holiday_id = :holiday_id;
    """

    row = db.execute(text(query), {"holiday_id": holiday_id}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Holiday not found")

    return dict(row._mapping)



