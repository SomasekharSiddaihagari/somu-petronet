import json
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.MOC.MoCCloser import MoCClosureCreate, MoCClosureUpdate


# ============================================================
# 🔹 CREATE FUNCTION
# ============================================================
def create_moc_closure(db: Session, moc_data: MoCClosureCreate):
    """
    Create a new MoC Closure record using PostgreSQL function.
    Uses DATE-only fields for date columns.
    """
    sql = text("""
        SELECT * FROM create_moc_closure(
            :p_moc_request_id,
            :p_moc_request_no,
            :p_title_of_moc,
            :p_date,
            :p_brief_description,
            :p_moc_initiator_dept,
            :p_executing_dept,
            :p_moc_execution_details,
            :p_job_start_date,
            :p_job_completion_date,
            :p_hira_recommendation_status,
            :p_revised_operating_procedure,
            :p_training_completed,
            :p_relevant_manuals,
            :p_comments_initiator,
            :p_status
        );
    """)

    params = {
        "p_moc_request_id": moc_data.moc_request_id,
        "p_moc_request_no": moc_data.moc_request_no,
        "p_title_of_moc": moc_data.title_of_moc,
        "p_date": moc_data.date,
        "p_brief_description": moc_data.brief_description,
        "p_moc_initiator_dept": moc_data.moc_initiator_dept,
        "p_executing_dept": moc_data.executing_dept,
        "p_moc_execution_details": moc_data.moc_execution_details,
        "p_job_start_date": moc_data.job_start_date,
        "p_job_completion_date": moc_data.job_completion_date,
        "p_hira_recommendation_status": moc_data.hira_recommendation_status,
        "p_revised_operating_procedure": moc_data.revised_operating_procedure,
        "p_training_completed": moc_data.training_completed,
        "p_relevant_manuals": json.dumps(moc_data.relevant_manuals) if moc_data.relevant_manuals else None,
        "p_comments_initiator": moc_data.comments_initiator,
        "p_status": moc_data.status
    }

    try:
        result = db.execute(sql, params)
        created = result.mappings().fetchone()

        if not created:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create MOC Closure record"
            )

        db.commit()
        return dict(created)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error during creation: {str(e)}"
        )


# ============================================================
# 🔹 UPDATE FUNCTION (by moc_request_id)
# ============================================================
def update_moc_closure_by_request_id(db: Session, moc_request_id: int, moc_data: MoCClosureUpdate):
    """
    Update an existing MoC Closure using PostgreSQL function.
    Updates all columns for the specified moc_request_id.
    Only DATEs (not timestamps) are used for date fields.
    """
    sql = text("""
        SELECT * FROM update_moc_closure_by_request_id(
            :p_moc_request_id,
            :p_moc_request_no,
            :p_title_of_moc,
            :p_date,
            :p_brief_description,
            :p_moc_initiator_dept,
            :p_executing_dept,
            :p_moc_execution_details,
            :p_job_start_date,
            :p_job_completion_date,
            :p_hira_recommendation_status,
            :p_revised_operating_procedure,
            :p_training_completed,
            :p_relevant_manuals,
            :p_comments_initiator,
            :p_status
        );
    """)

    params = {
        "p_moc_request_id": moc_request_id,
        "p_moc_request_no": moc_data.moc_request_no,
        "p_title_of_moc": moc_data.title_of_moc,
        "p_date": moc_data.date,
        "p_brief_description": moc_data.brief_description,
        "p_moc_initiator_dept": moc_data.moc_initiator_dept,
        "p_executing_dept": moc_data.executing_dept,
        "p_moc_execution_details": moc_data.moc_execution_details,
        "p_job_start_date": moc_data.job_start_date,
        "p_job_completion_date": moc_data.job_completion_date,
        "p_hira_recommendation_status": moc_data.hira_recommendation_status,
        "p_revised_operating_procedure": moc_data.revised_operating_procedure,
        "p_training_completed": moc_data.training_completed,
        "p_relevant_manuals": json.dumps(moc_data.relevant_manuals) if moc_data.relevant_manuals else None,
        "p_comments_initiator": moc_data.comments_initiator,
        "p_status": moc_data.status
    }

    try:
        result = db.execute(sql, params)
        updated = result.mappings().fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No MOC Closure found with moc_request_id = {moc_request_id}"
            )

        db.commit()
        return dict(updated)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error during update: {str(e)}"
        )
