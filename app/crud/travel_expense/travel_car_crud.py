from sqlalchemy.orm import Session
from sqlalchemy import text


# ----------------------------------------------------------
#                     CREATE CAR
# ----------------------------------------------------------
def create_car(db: Session, data):
    insert_sql = text("""
        INSERT INTO travel_requisition_car
        (requisition_id, city, car_from, car_to, car_type, car_remarks)
        VALUES (:requisition_id, :city, :car_from, :car_to, :car_type, :car_remarks)
        RETURNING trc_id;
    """)

    result = db.execute(insert_sql, data.dict())
    trc_id = result.fetchone()[0]

    # Insert into history
    history_sql = text("""
        INSERT INTO travel_requisition_car_history
        (requisition_id, city, car_from, car_to, car_type, car_remarks)
        VALUES (:requisition_id, :city, :car_from, :car_to, :car_type, :car_remarks)
    """)
    db.execute(history_sql, data.dict())
    db.commit()

    # Fetch saved row
    row = db.execute(
        text("SELECT * FROM travel_requisition_car WHERE trc_id = :trc_id"),
        {"trc_id": trc_id}
    ).fetchone()

    return dict(row._mapping)


# ----------------------------------------------------------
#                     UPDATE CAR
# ----------------------------------------------------------
def update_car(db: Session, trc_id: int, data):
    old = db.execute(
        text("SELECT * FROM travel_requisition_car WHERE trc_id = :trc_id"),
        {"trc_id": trc_id}
    ).fetchone()

    if not old:
        return None

    db.execute(text("""
        INSERT INTO travel_requisition_car_history
        (requisition_id, city, car_from, car_to, car_type, car_remarks)
        VALUES (:requisition_id, :city, :car_from, :car_to, :car_type, :car_remarks)
    """), dict(old._mapping))

    update_sql = text("""
        UPDATE travel_requisition_car
        SET requisition_id=:requisition_id,
            city=:city,
            car_from=:car_from,
            car_to=:car_to,
            car_type=:car_type,
            car_remarks=:car_remarks
        WHERE trc_id=:trc_id
    """)

    params = data.dict()
    params["trc_id"] = trc_id

    db.execute(update_sql, params)
    db.commit()

    row = db.execute(
        text("SELECT * FROM travel_requisition_car WHERE trc_id = :trc_id"),
        {"trc_id": trc_id}
    ).fetchone()

    return dict(row._mapping)


# ----------------------------------------------------------
#                     DELETE CAR
# ----------------------------------------------------------
def delete_car(db: Session, trc_id: int):
    db.execute(text("DELETE FROM travel_requisition_car WHERE trc_id = :trc_id"),
               {"trc_id": trc_id})
    db.commit()
    return {"deleted": True}
