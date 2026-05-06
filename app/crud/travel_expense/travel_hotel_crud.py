from sqlalchemy.orm import Session
from sqlalchemy import text


# ----------------------------------------------------------
#                     CREATE HOTEL
# ----------------------------------------------------------
def create_hotel(db: Session, data):
    insert_sql = text("""
        INSERT INTO travel_requisition_hotel
        (requisition_id, city, hotel_name, hotel_remarks)
        VALUES (:requisition_id, :city, :hotel_name, :hotel_remarks)
        RETURNING trh_id;
    """)

    result = db.execute(insert_sql, data.dict())
    trh_id = result.fetchone()[0]

    # Insert into history
    history_sql = text("""
        INSERT INTO travel_requisition_hotel_history
        (requisition_id, city, hotel_name, hotel_remarks)
        VALUES (:requisition_id, :city, :hotel_name, :hotel_remarks)
    """)
    db.execute(history_sql, data.dict())
    db.commit()

    # Fetch complete row
    row = db.execute(
        text("SELECT * FROM travel_requisition_hotel WHERE trh_id = :trh_id"),
        {"trh_id": trh_id}
    ).fetchone()

    return dict(row._mapping)


# ----------------------------------------------------------
#                     UPDATE HOTEL
# ----------------------------------------------------------
def update_hotel(db: Session, trh_id: int, data):
    old = db.execute(
        text("SELECT * FROM travel_requisition_hotel WHERE trh_id = :trh_id"),
        {"trh_id": trh_id}
    ).fetchone()

    if not old:
        return None

    # Insert old data into history
    db.execute(text("""
        INSERT INTO travel_requisition_hotel_history
        (requisition_id, city, hotel_name, hotel_remarks)
        VALUES (:requisition_id, :city, :hotel_name, :hotel_remarks)
    """), dict(old._mapping))

    update_sql = text("""
        UPDATE travel_requisition_hotel
        SET requisition_id=:requisition_id,
            city=:city,
            hotel_name=:hotel_name,
            hotel_remarks=:hotel_remarks
        WHERE trh_id=:trh_id
    """)

    params = data.dict()
    params["trh_id"] = trh_id

    db.execute(update_sql, params)
    db.commit()

    # Fetch updated row
    row = db.execute(
        text("SELECT * FROM travel_requisition_hotel WHERE trh_id = :trh_id"),
        {"trh_id": trh_id}
    ).fetchone()

    return dict(row._mapping)


# ----------------------------------------------------------
#                     DELETE HOTEL
# ----------------------------------------------------------
def delete_hotel(db: Session, trh_id: int):
    db.execute(text("DELETE FROM travel_requisition_hotel WHERE trh_id = :trh_id"),
               {"trh_id": trh_id})
    db.commit()
    return {"deleted": True}
