from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.travel_expense.travel_expense_schema import (
    TravelExpenseSheetCreate,
    TravelExpenseSheetUpdate,
)


# ----------------------------------------------------------
# POST → CREATE MAIN + HISTORY (Force approval fields NULL)
# ----------------------------------------------------------
def create_travel_expense_sheet(db: Session, data: TravelExpenseSheetCreate):

    payload = data.dict()

    # Force NULL workflow dates on CREATE
    payload["updated_by_supervisor"] = None
    payload["updated_by_hr"] = None
    payload["updated_by_md"] = None
    payload["updated_by_finance"] = None

    insert_main_sql = text("""
        INSERT INTO travel_expense_sheet
        (
            requisition_number, user_id,travel_id, employee_name, employee_number, designation, grade, station, department,
            travel_mode, purpose_of_travel, violation, total_excl_gst, total_gst, total_incl_gst,
            advance_taken, amount_payable_receivable, comments, status,is_dollar,
            updated_by_supervisor, updated_by_supervisor_name, supervisor_comments,
            updated_by_head_tech, updated_by_head_tech_name, head_tech_comments,
            updated_by_hr, updated_by_hr_name, hr_comments,
            updated_by_md, updated_by_md_name, md_comment,
            updated_by_finance, updated_by_finance_name, finance_comments
        )
        VALUES
        (
            :requisition_number, :user_id, :travel_id,:employee_name, :employee_number, :designation, :grade, :station,
            :department, :travel_mode, :purpose_of_travel, :violation, :total_excl_gst, :total_gst,
            :total_incl_gst, :advance_taken, :amount_payable_receivable, :comments, :status,:is_dollar,
            :updated_by_supervisor, :updated_by_supervisor_name, :supervisor_comments,
            :updated_by_head_tech, :updated_by_head_tech_name, :head_tech_comments,
            :updated_by_hr, :updated_by_hr_name, :hr_comments,
            :updated_by_md, :updated_by_md_name, :md_comment,
            :updated_by_finance, :updated_by_finance_name, :finance_comments
        )
        RETURNING tes_id;
    """)

    result = db.execute(insert_main_sql, payload)
    new_id = result.fetchone()[0]

    # History payload
    history_data = payload.copy()
    history_data["expense_sheet_id"] = new_id

    insert_history_sql = text("""
        INSERT INTO travel_expense_sheet_history
        (
            expense_sheet_id, user_id, requisition_number, violation,
            employee_name, employee_number, designation, grade, station, department,
            travel_mode, purpose_of_travel,
            total_excl_gst, total_gst, total_incl_gst, advance_taken, amount_payable_receivable,
            comments, status,
            updated_by_supervisor, updated_by_supervisor_name, supervisor_comments,
            updated_by_head_tech, updated_by_head_tech_name, head_tech_comments,
            updated_by_hr, updated_by_hr_name, hr_comments,
            updated_by_md, updated_by_md_name,
            updated_by_finance, updated_by_finance_name, finance_comments
        )
        VALUES
        (
            :expense_sheet_id, :user_id, :requisition_number, :violation,
            :employee_name, :employee_number, :designation, :grade, :station, :department,
            :travel_mode, :purpose_of_travel,
            :total_excl_gst, :total_gst, :total_incl_gst, :advance_taken, :amount_payable_receivable,
            :comments, :status,
            :updated_by_supervisor, :updated_by_supervisor_name, :supervisor_comments,
            :updated_by_head_tech, :updated_by_head_tech_name, :head_tech_comments,
            :updated_by_hr, :updated_by_hr_name, :hr_comments,
            :updated_by_md, :updated_by_md_name,
            :updated_by_finance, :updated_by_finance_name, :finance_comments
        )
    """)

    db.execute(insert_history_sql, history_data)
    db.commit()

    return {
    "tes_id": new_id,
    "requisition_number": data.requisition_number,
    "user_id": data.user_id,
    "status": "TC Pending - Supervisor",
    "violation": data.violation,
    "station": data.station,
}



# ----------------------------------------------------------
# PUT → PARTIAL UPDATE (ONLY fields sent by client)
# ----------------------------------------------------------
def update_travel_expense_sheet(db: Session, tes_id: int, data: TravelExpenseSheetUpdate):

    # Only take fields actually sent by client
    payload = data.dict(exclude_unset=True)

    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{key} = :{key}" for key in payload.keys()])

    update_sql = text(f"""
        UPDATE travel_expense_sheet 
        SET {set_clause}
        WHERE tes_id = :tes_id
    """)

    payload["tes_id"] = tes_id

    db.execute(update_sql, payload)
    db.commit()

    return {"message": "Updated successfully"}
