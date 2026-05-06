from sqlalchemy import text
from sqlalchemy.orm import Session


# ---------------- CREATE ----------------
from sqlalchemy import text

from sqlalchemy import text

def create_travel_requisition(db: Session, data):

    insert_sql = text("""
        INSERT INTO travel_requisition (
            user_id, employee_name, employee_number, designation, grade,
            station, department, purpose_of_travel, status, approver_comments,
            visa_for, emigration_required, foreign_exchange
        ) VALUES (
            :user_id, :employee_name, :employee_number, :designation, :grade,
            :station, :department, :purpose_of_travel, :status, :approver_comments,
            :visa_for, :emigration_required, :foreign_exchange
        )
        RETURNING *;
    """)

    params = data.dict()
    row = db.execute(insert_sql, params).fetchone()

    if not row:
        return None

    new_row = dict(row._mapping)   # FIX ✔

    travel_id = new_row["travel_id"]

    history_sql = text("""
        INSERT INTO travel_requisition_history (
            requisition_id, employee_name, employee_number, designation,
            grade, station, department, purpose_of_travel, visa_for,
            emigration_required, foreign_exchange, status, approver_comments,
            updated_at
        )
        VALUES (
            :travel_id, :employee_name, :employee_number, :designation,
            :grade, :station, :department, :purpose_of_travel, :visa_for,
            :emigration_required, :foreign_exchange, :status, :approver_comments,
            NOW()
        );
    """)

    db.execute(history_sql, {**params, "travel_id": travel_id})
    db.commit()

    return new_row

# ---------------- UPDATE ----------------
from sqlalchemy import text

from sqlalchemy import text

from sqlalchemy import text

def update_travel_requisition(db: Session, travel_id: int, data):

    update_sql = text("""
        UPDATE travel_requisition
        SET
            user_id = :user_id,
            employee_name = :employee_name,
            employee_number = :employee_number,
            designation = :designation,
            grade = :grade,
            station = :station,
            department = :department,
            purpose_of_travel = :purpose_of_travel,
            status = :status,
            approver_comments = :approver_comments,
            visa_for = :visa_for,
            emigration_required = :emigration_required,
            foreign_exchange = :foreign_exchange,
            updated_at = NOW()
           
        WHERE travel_id = :travel_id
        RETURNING *;
    """)

    params = data.dict()
    params["travel_id"] = travel_id

    row = db.execute(update_sql, params).fetchone()

    if not row:
        return None

    updated_row = dict(row._mapping)   # FIX ✔

    # Insert into history table
    history_sql = text("""
        INSERT INTO travel_requisition_history (
            requisition_id, employee_name, employee_number, designation,
            grade, station, department, purpose_of_travel, visa_for,
            emigration_required, foreign_exchange, status, approver_comments,
            updated_at
        )
        VALUES (
            :travel_id, :employee_name, :employee_number, :designation,
            :grade, :station, :department, :purpose_of_travel, :visa_for,
            :emigration_required, :foreign_exchange, :status, :approver_comments,
            NOW()
        );
    """)

    db.execute(history_sql, params)
    db.commit()

    return updated_row


# ---------------- GET (Already Working) ----------------
def get_travel_requisition_full(db: Session, travel_id: int):

    sql = text("""
        SELECT get_travel_requisition_full_fn(:travel_id) AS result;
    """)

    row = db.execute(sql, {"travel_id": travel_id}).fetchone()

    if not row:
        return None

    result_json = row[0]

    if not result_json:
        return None

    return result_json
