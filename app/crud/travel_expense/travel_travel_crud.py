from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime


def create_travel(db: Session, data):
    insert_sql = text("""
        INSERT INTO travel_requisition_travel
        (requisition_id, from_location, to_location, travel_date, to_date,
         flight_train_number, class_of_travel, travel_remarks)
        VALUES (:requisition_id, :from_location, :to_location, :travel_date, :to_date,
         :flight_train_number, :class_of_travel, :travel_remarks)
        RETURNING trt_id;
    """)

    result = db.execute(insert_sql, data.dict())
    trt_id = result.fetchone()[0]

    # history insert
    history_sql = text("""
        INSERT INTO travel_requisition_travel_history
        (requisition_id, from_location, to_location, travel_date, to_date,
         flight_train_number, class_of_travel, travel_remarks)
        VALUES (:requisition_id, :from_location, :to_location, :travel_date, :to_date,
         :flight_train_number, :class_of_travel, :travel_remarks)
    """)
    db.execute(history_sql, data.dict())
    db.commit()

    # fetch full row
    fetch_sql = text("SELECT * FROM travel_requisition_travel WHERE trt_id = :trt_id")
    row = db.execute(fetch_sql, {"trt_id": trt_id}).fetchone()

    return dict(row._mapping)

def update_travel(db: Session, trt_id: int, data):
    old_sql = text("SELECT * FROM travel_requisition_travel WHERE trt_id = :trt_id")
    old = db.execute(old_sql, {"trt_id": trt_id}).fetchone()

    if not old:
        return None

    # insert OLD data into history
    db.execute(text("""
        INSERT INTO travel_requisition_travel_history
        (requisition_id, from_location, to_location, travel_date, to_date,
         flight_train_number, class_of_travel, travel_remarks)
        VALUES (:requisition_id, :from_location, :to_location, :travel_date, :to_date,
         :flight_train_number, :class_of_travel, :travel_remarks)
    """), dict(old._mapping))

    update_sql = text("""
        UPDATE travel_requisition_travel
        SET requisition_id=:requisition_id,
            from_location=:from_location,
            to_location=:to_location,
            travel_date=:travel_date,
            to_date=:to_date,
            flight_train_number=:flight_train_number,
            class_of_travel=:class_of_travel,
            travel_remarks=:travel_remarks
        WHERE trt_id=:trt_id
    """)

    params = data.dict()
    params["trt_id"] = trt_id

    db.execute(update_sql, params)
    db.commit()

    fetch_sql = text("SELECT * FROM travel_requisition_travel WHERE trt_id = :trt_id")
    row = db.execute(fetch_sql, {"trt_id": trt_id}).fetchone()

    return dict(row._mapping)

def delete_travel(db: Session, trt_id: int):
    delete_sql = text("DELETE FROM travel_requisition_travel WHERE trt_id = :trt_id")
    db.execute(delete_sql, {"trt_id": trt_id})
    db.commit()
    return {"deleted": True}
