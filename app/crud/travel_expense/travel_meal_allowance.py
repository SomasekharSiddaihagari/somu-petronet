from sqlalchemy.orm import Session
from app.models.travel_expense.meal_allowance import MealAllowanceSheet
from app.models.travel_expense.meal_allowance_sheet_history import MealAllowanceSheetHistory
from app.models.travel_expense.meal_allowance_sheet_detail import MealAllowanceSheetDetail
from app.models.travel_expense.meal_allowance_sheet_detail_history import MealAllowanceSheetDetailHistory
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
def create_meal_sheet(db: Session, data: dict):
    data.pop("requisition_number", None)  # DB default

    columns = ", ".join(data.keys())
    values = ", ".join([f":{key}" for key in data])

    sql = text(f"""
        INSERT INTO meal_allowance_sheet ({columns})
        VALUES ({values})
        RETURNING *;
    """)

    result = db.execute(sql, data)
    row = result.fetchone()
    db.commit()
    return dict(row._mapping)
def update_meal_sheet(db: Session, meal_sheet_id: int, data: dict):
    if not data:
        return None

    set_clause = ", ".join([f"{key} = :{key}" for key in data])
    data["meal_sheet_id"] = meal_sheet_id

    sql = text(f"""
        UPDATE meal_allowance_sheet
        SET {set_clause}
        WHERE meal_sheet_id = :meal_sheet_id
        RETURNING *;
    """)

    result = db.execute(sql, data)
    row = result.fetchone()
    if not row:
        return None

    db.commit()
    return dict(row._mapping)



# def delete_meal_sheet(db: Session, meal_sheet_id: int):
#     sheet = db.query(MealAllowanceSheet).filter(
#         MealAllowanceSheet.meal_sheet_id == meal_sheet_id
#     ).first()

#     if not sheet:
#         return None

#     deleted_id = sheet.meal_sheet_id
#     db.delete(sheet)
#     db.commit()

#     return deleted_id
  




def create_meal_detail(db: Session, data: dict):
    detail = MealAllowanceSheetDetail(**data)
    db.add(detail)
    db.commit()
    db.refresh(detail)

    history = MealAllowanceSheetDetailHistory(
        meal_sheet_id=detail.meal_sheet_id,
        date=detail.date,
        from_time=detail.from_time,            
        to_time=detail.to_time,                
        travel_route=detail.travel_route,
        time_duration=detail.time_duration,
        distance_from_station=detail.distance_from_station,
        purpose=detail.purpose,
        meal_amount=detail.meal_amount,
        meal_gst=detail.meal_gst,
        meal_total=detail.meal_total,
        meal_proof=detail.meal_proof,
        remarks=detail.remarks
    )

    db.add(history)
    db.commit()

    return detail


# ---------------- UPDATE ----------------
def update_meal_detail(db: Session, detail_id: int, data: dict):
    detail = db.query(MealAllowanceSheetDetail).filter(
        MealAllowanceSheetDetail.meal_sheet_detail_id == detail_id
    ).first()

    if not detail:
        return None

    for key, value in data.items():
        setattr(detail, key, value)

    db.commit()
    db.refresh(detail)

    history = MealAllowanceSheetDetailHistory(
        meal_sheet_id=detail.meal_sheet_id,
        date=detail.date,
        from_time=detail.from_time,            
        to_time=detail.to_time,                
        travel_route=detail.travel_route,
        time_duration=detail.time_duration,
        distance_from_station=detail.distance_from_station,
        purpose=detail.purpose,
        meal_amount=detail.meal_amount,
        meal_gst=detail.meal_gst,
        meal_total=detail.meal_total,
        meal_proof=detail.meal_proof,
        remarks=detail.remarks
    )

    db.add(history)
    db.commit()

    return detail


# ---------------- DELETE ----------------
def delete_meal_detail(db: Session, detail_id: int):
    detail = db.query(MealAllowanceSheetDetail).filter(
        MealAllowanceSheetDetail.meal_sheet_detail_id == detail_id
    ).first()

    if not detail:
        return False

    db.delete(detail)
    db.commit()

    return True
