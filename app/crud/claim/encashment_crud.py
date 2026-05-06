from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.claim.encashment_schemas import (
    EncashmentMainCreate,
    EncashmentMainUpdate,
    LeaveEncashmentCreate,
    LeaveEncashmentUpdate,
)



def generate_encashment_ref(db: Session) -> str:
    year = datetime.now().year
    prefix = f"ENC/{year}/"

    query = text("""
        SELECT encashment_ref_id
        FROM encashment_main
        WHERE encashment_ref_id LIKE :prefix
        ORDER BY encashment_main_id DESC
        LIMIT 1
    """)

    last = db.execute(query, {"prefix": f"{prefix}%"}).fetchone()

    next_no = 1
    if last and last[0]:
        next_no = int(last[0].split("/")[-1]) + 1

    return f"{prefix}{str(next_no).zfill(6)}"




# =================================================
# ENCASHMENT MAIN
# =================================================
def create_encashment_main(db: Session, data: EncashmentMainCreate):
    encashment_ref_id = generate_encashment_ref(db)

    payload = data.model_dump()
    payload["encashment_ref_id"] = encashment_ref_id

    query = text("""
        INSERT INTO encashment_main (
            encashment_ref_id,
            employee_name,
            employee_code,
            department,
            designation,
            station,
            grade,
            claim_module,
            status,
            created_by
        )
        VALUES (
            :encashment_ref_id,
            :employee_name,
            :employee_code,
            :department,
            :designation,
            :station,
            :grade,
            :claim_module,
            :status,
            :created_by
        )
        RETURNING encashment_main_id
    """)

    encashment_main_id = db.execute(query, payload).scalar()

    insert_encashment_main_history(db, encashment_main_id)  # type: ignore
    db.commit()
    return encashment_main_id



def update_encashment_main(
    db: Session,
    encashment_main_id: int,
    data: EncashmentMainUpdate
):
    update_fields = data.model_dump(exclude_unset=True)
    if not update_fields:
        return False

    set_clause = ", ".join(f"{k} = :{k}" for k in update_fields)
    query = text(f"""
        UPDATE encashment_main
        SET {set_clause}
        WHERE encashment_main_id = :encashment_main_id
    """)
    update_fields["encashment_main_id"] = encashment_main_id
    db.execute(query, update_fields)

    insert_encashment_main_history(db, encashment_main_id)
    db.commit()
    return True


def insert_encashment_main_history(db: Session, encashment_main_id: int):
    db.execute(text("""
        INSERT INTO encashment_main_history (
            encashment_main_id,
            encashment_ref_id,
            employee_name,
            employee_code,
            department,
            designation,
            station,
            grade,
            claim_module,
            status,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            updated_at
        )
        SELECT
            encashment_main_id,
            encashment_ref_id,
            employee_name,
            employee_code,
            department,
            designation,
            station,
            grade,
            claim_module,
            status,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            NOW()
        FROM encashment_main
        WHERE encashment_main_id = :id
    """), {"id": encashment_main_id})


# =================================================
# LEAVE ENCASHMENT SUBMISSION
# =================================================
def create_leave_encashment(db: Session, data: LeaveEncashmentCreate):
    query = text("""
        INSERT INTO leave_encashment (
            encashment_ref_id,
            encashment_main_id,
            employee_name,
            employee_code,
            designation,
            station,
            encashment_date,
            leave_type,
            el_encashable,
            encashment_opening,
            non_encashment_opening,
            total_encashment_opening,
            encash_el,
                 no_days_approved,
            balance_as_on_date,
            request_text,
            declaration_accepted,
            status,
            created_by,
            updated_by
        )
        VALUES (
            :encashment_ref_id,
            :encashment_main_id,
            :employee_name,
            :employee_code,
            :designation,
            :station,
            :encashment_date,
            :leave_type,
            :el_encashable,
            :encashment_opening,
            :non_encashment_opening,
            :total_encashment_opening,
            :encash_el,
                 :no_days_approved,
            :balance_as_on_date,
            :request_text,
            :declaration_accepted,
            :status,
            :created_by,
            :updated_by
        )
        RETURNING leave_encashment_id
    """)

    payload = data.model_dump()
    leave_encashment_id = db.execute(query, payload).scalar()

    insert_leave_encashment_history(db, leave_encashment_id)
    db.commit()
    return leave_encashment_id


# =================================================
# UPDATE LEAVE ENCASHMENT
# =================================================
def update_leave_encashment(
    db: Session,
    leave_encashment_id: int,
    data: LeaveEncashmentUpdate
):
    update_fields = data.model_dump(exclude_unset=True)

    if not update_fields:
        return False

    set_clause = ", ".join(f"{k} = :{k}" for k in update_fields)

    query = text(f"""
        UPDATE leave_encashment
        SET {set_clause}
        WHERE leave_encashment_id = :leave_encashment_id
    """)

    update_fields["leave_encashment_id"] = leave_encashment_id
    db.execute(query, update_fields)

    insert_leave_encashment_history(db, leave_encashment_id)
    db.commit()
    return True


# =================================================
# INSERT LEAVE ENCASHMENT HISTORY (SNAPSHOT)
# =================================================
def insert_leave_encashment_history(db: Session, leave_encashment_id: int):
    history_sql = text("""
        INSERT INTO leave_encashment_history (
            leave_encashment_id,
            encashment_ref_id,
            employee_name,
            employee_code,
            designation,
            station,
            encashment_date,
            leave_type,
            el_encashable,
            encash_el,
            encashment_opening,
            non_encashment_opening,
            total_encashment_opening,
            balance_as_on_date,
            request_text,
            declaration_accepted,
            status,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            updated_at
        )
        SELECT
            leave_encashment_id,
            encashment_ref_id,
            employee_name,
            employee_code,
            designation,
            station,
            encashment_date,
            leave_type,
            el_encashable,
            encash_el,
            encashment_opening,
            non_encashment_opening,
            total_encashment_opening,
            balance_as_on_date,
            request_text,
            declaration_accepted,
            status,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            NOW()
        FROM leave_encashment
        WHERE leave_encashment_id = :id
    """)

    db.execute(history_sql, {"id": leave_encashment_id})