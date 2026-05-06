from datetime import datetime
import json
from sqlalchemy import text
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.MOC.MOCSchema import MOCRequest, MOCStatusCountRequest, MOCRequestDetail, MOCStatusCountRequestStation


def insert_moc_request_service(
    db: Session,
    req: MOCRequest
    ):
    try:
        # ------------------------------------------------------------
        # 0️⃣ Basic validation
        # ------------------------------------------------------------
        if not req.created_by:
            raise Exception("created_by is required in request payload")

        # ------------------------------------------------------------
        # 1️⃣ Resolve user_id from created_by
        # ------------------------------------------------------------
        user_id_sql = text("""
    SELECT user_id
    FROM public.users
    WHERE username = :username
    LIMIT 1
    """)
 
        user_id = db.execute(
            user_id_sql,
            {"username": req.created_by}
    ).scalar()

        if not user_id:
            raise Exception(
                f"User not found for username: {req.created_by}"
            )

        # ------------------------------------------------------------
        # 2️⃣ Generate MOC request number
        # ------------------------------------------------------------
        moc_no_sql = text("""
            SELECT public.generate_moc_request_no(:user_id)
        """)

        moc_request_no = db.execute(
            moc_no_sql,
            {"user_id": user_id}
        ).scalar_one()

        # ------------------------------------------------------------
        # 3️⃣ Prepare parameters (IMPORTANT PART)
        # ------------------------------------------------------------
        params = req.dict(exclude_unset=True)

        OPTIONAL_FIELDS = [
            "reviewer_comments",
            "approver_comments",
            "sic_comments",
            "attachments",
            "comments",
            "hira_approved_date",
            "sic_approved_date",
            "approved_date",
            "closure_date",
            "closure_comments",
            "objectives_achieved",
            "other_aspects",
            "other_units_impacted",
            "statutory_approval_details",
        ]

        # Ensure all optional SQL binds exist
        for field in OPTIONAL_FIELDS:
            params.setdefault(field, None)

        params.update({
            "moc_request_no": moc_request_no,
            "created_by": req.created_by,
            "updated_by": req.updated_by or req.created_by
        })

        # ------------------------------------------------------------
        # 4️⃣ Insert into moc_requests
        # ------------------------------------------------------------
        insert_moc_sql = text("""
            INSERT INTO public.moc_requests (
                moc_request_no,
                station_name,
                title,
                "date",
                priority,
                modification_type,
                time_limit,
                shutdown_required,
                present_system,
                proposed_change,
                justification,
                objectives,
                other_units_impacted,
                statutory_approval_required,
                statutory_approval_details,
                impact_of_modification,
                short_text,
                consequences_non_implementation,
                hse,
                efficiency,
                quality,
                reliability,
                other_aspects_required,
                other_aspects,
                objectives_achieved,
                attachments,
                comments,

                reviewer_comments,
                approver_comments,
                sic_comments,

                status,
                is_active,
                submission_date,

                hira_approved_date,
                sic_approved_date,
                approved_date,
                closure_date,
                closure_comments,

                created_by,
                updated_by,
                created_at,
                updated_at
            )
            VALUES (
                :moc_request_no,
                :station_name,
                :title,
                :date,
                :priority,
                :modification_type,
                :time_limit,
                :shutdown_required,
                :present_system,
                :proposed_change,
                :justification,
                :objectives,
                :other_units_impacted,
                :statutory_approval_required,
                :statutory_approval_details,
                :impact_of_modification,
                :short_text,
                :consequences_non_implementation,
                :hse,
                :efficiency,
                :quality,
                :reliability,
                :other_aspects_required,
                :other_aspects,
                :objectives_achieved,
                :attachments,
                :comments,

                :reviewer_comments,
                :approver_comments,
                :sic_comments,

                :status,
                :is_active,
                :submission_date,

                :hira_approved_date,
                :sic_approved_date,
                :approved_date,
                :closure_date,
                :closure_comments,

                :created_by,
                :updated_by,
                NOW(),
                NOW()
            )
            RETURNING *;
        """)

        inserted_row = db.execute(
            insert_moc_sql,
            params
        ).mappings().one()

        # ------------------------------------------------------------
        # 5️⃣ Insert snapshot into moc_request_history
        # ------------------------------------------------------------
        history_sql = text("""
            INSERT INTO public.moc_request_history (
                moc_request_no,
                station_name,
                title,
                "date",
                priority,
                modification_type,
                time_limit,
                shutdown_required,
                present_system,
                proposed_change,
                justification,
                objectives,
                other_units_impacted,
                statutory_approval_required,
                statutory_approval_details,
                impact_of_modification,
                short_text,
                consequences_non_implementation,
                hse,
                efficiency,
                quality,
                reliability,
                other_aspects_required,
                other_aspects,
                objectives_achieved,
                attachments,
                comments,

                reviewer_comments,
                approver_comments,
                sic_comments,

                status,
                is_active,
                submission_date,

                hira_approved_date,
                sic_approved_date,
                approved_date,
                closure_date,
                closure_comments,

                created_by,
                updated_by,
                created_at,
                updated_at
            )
            SELECT
                moc_request_no,
                station_name,
                title,
                "date",
                priority,
                modification_type,
                time_limit,
                shutdown_required,
                present_system,
                proposed_change,
                justification,
                objectives,
                other_units_impacted,
                statutory_approval_required,
                statutory_approval_details,
                impact_of_modification,
                short_text,
                consequences_non_implementation,
                hse,
                efficiency,
                quality,
                reliability,
                other_aspects_required,
                other_aspects,
                objectives_achieved,
                attachments,
                comments,

                reviewer_comments,
                approver_comments,
                sic_comments,

                status,
                is_active,
                submission_date,

                hira_approved_date,
                sic_approved_date,
                approved_date,
                closure_date,
                closure_comments,

                created_by,
                updated_by,
                created_at,
                updated_at
            FROM public.moc_requests
            WHERE moc_request_no = :moc_request_no
        """)

        db.execute(
            history_sql,
            {"moc_request_no": moc_request_no}
        )

        # ------------------------------------------------------------
        # 6️⃣ Commit
        # ------------------------------------------------------------
        db.commit()

        return {
            "status": "0000 | Success",
            "data": dict(inserted_row)
        }

    except Exception as e:
        db.rollback()
        raise e
    
    


# def get_moc_request_by_no(db: Session, moc_request_no: str) -> Optional[MOCRequestDetail]:
#     """
#     Fetch a single MOC request record by its request number.
#     Assumes a PostgreSQL function `public.get_moc_request(:moc_request_no)` returns JSON-like records.
#     """
#     try:
#         moc_request_no = moc_request_no.strip()
#         sql = text("SELECT * FROM public.get_moc_request(:moc_request_no);")
#         result = db.execute(sql, {"moc_request_no": moc_request_no})
#         rows = result.fetchall()

#         if not rows:
#             return None

#         # Convert each row into a dict
#         moc_records = [dict(row._mapping) for row in rows]

#         # If function returns multiple rows, assume first one is main record
#         moc_record = moc_records[0]

#         # Parse hira_entries if stored as JSON string
#         # Parse hira_entries if stored as JSON string
#         # Parse hira_entries if stored as JSON string
#         if "hira_entries" in moc_record and moc_record["hira_entries"] and isinstance(moc_record["hira_entries"], str):
#             try:
#                 moc_record["hira_entries"] = json.loads(moc_record["hira_entries"])
#             except json.JSONDecodeError:
#                 moc_record["hira_entries"] = []

#         # Sort hira_entries by hira_id ascending
#         if moc_record.get("hira_entries"):
#             moc_record["hira_entries"] = sorted(
#                 moc_record["hira_entries"],
#                 key=lambda x: x.get("hira_id") or 0
#             )

#         # ============================
#         # Parse closure_data if stored as JSON string
#         # ============================
#         if "closure_data" in moc_record and moc_record["closure_data"]:
#             if isinstance(moc_record["closure_data"], str):
#                 try:
#                     moc_record["closure_data"] = json.loads(moc_record["closure_data"])
#                 except json.JSONDecodeError:
#                     moc_record["closure_data"] = {}
#             # Extract closure_date and closure_comments from closure_data
#             if isinstance(moc_record["closure_data"], dict):
#                 moc_record["closure_date"] = moc_record["closure_data"].get("job_completion_date")
#                 moc_record["closure_comments"] = moc_record["closure_data"].get("comments_initiator")
#         else:
#             moc_record["closure_data"] = {}
#         # ============================
#         # Helper: fetch designation by user_id
#         # ============================
#         def get_designation_by_id(user_id):
#             if not user_id:
#                 return None
#             row = db.execute(
#                 text("SELECT designation FROM users WHERE user_id = :uid"),
#                 {"uid": user_id}
#             ).fetchone()
#             return row.designation if row else None

#         # ============================
#         # Helper: fetch designation by full name or username
#         # ============================
#         def get_designation_by_name(name):
#             if not name:
#                 return None
#             row = db.execute(
#                 text("""
#                     SELECT designation FROM users 
#                     WHERE CONCAT(first_name, ' ', last_name) = :name
#                     OR username = :name
#                 """),
#                 {"name": name}
#             ).fetchone()
#             return row.designation if row else None

#         # ============================
#         # Helper: fetch all reviewers by role_id=3 and submenu_id=2
#         # ============================
#         def get_reviewers():
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT
#                         u.user_id,
#                         CONCAT(u.first_name, ' ', u.last_name) AS full_name,
#                         u.designation
#                     FROM role_permissions rp
#                     JOIN users u ON u.user_id = rp.user_id
#                     WHERE rp.role_id = 3
#                     AND rp.submenu_id = 2
#                     AND u.is_deleted = false
#                 """)
#             ).fetchall()
#             return [
#                 {
#                     "reviewer_id": row.user_id,
#                     "reviewer_name": row.full_name,
#                     "reviewer_designation": row.designation
#                 }
#                 for row in rows
#             ]

#         # ============================
#         # Enrich with designations
#         # ============================
#         moc_record["hira_reviewer_designation"] = get_designation_by_id(moc_record.get("hira_reviewer_id"))
#         moc_record["sic_designation"] = get_designation_by_id(moc_record.get("sic_id"))
#         moc_record["approver_designation"] = get_designation_by_id(moc_record.get("approver_id"))
#         moc_record["created_by_designation"] = get_designation_by_name(moc_record.get("created_by"))

#         # ============================
#         # Enrich with all available reviewers
#         # ============================
#         moc_record["available_approver"] = get_reviewers()

#         return MOCRequestDetail(**moc_record)

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
def get_moc_request_by_no(db: Session, moc_request_no: str) -> Optional[MOCRequestDetail]:
    """
    Fetch a single MOC request record by its request number.
    Assumes a PostgreSQL function `public.get_moc_request(:moc_request_no)` returns JSON-like records.
    """
    try:
        moc_request_no = moc_request_no.strip()
        sql = text("SELECT * FROM public.get_moc_request(:moc_request_no);")

        result = db.execute(sql, {"moc_request_no": moc_request_no})
        rows = result.fetchall()

        if not rows:
            return None

        # Convert each row into a dict
        moc_records = [dict(row._mapping) for row in rows]

        # If function returns multiple rows, assume first one is main record
        moc_record = moc_records[0]
        if "short_text" not in moc_record or moc_record.get("short_text") is None:
            row = db.execute(
                text("SELECT short_text FROM public.moc_requests WHERE moc_request_no = :no"),
                {"no": moc_request_no}
            ).fetchone()
            if row:
                moc_record["short_text"] = row.short_text

        # Parse hira_entries if stored as JSON string
        if "hira_entries" in moc_record and moc_record["hira_entries"] and isinstance(moc_record["hira_entries"], str):
            try:
                moc_record["hira_entries"] = json.loads(moc_record["hira_entries"])
            except json.JSONDecodeError:
                moc_record["hira_entries"] = []

        # Sort hira_entries by hira_id ascending
        if moc_record.get("hira_entries"):
            moc_record["hira_entries"] = sorted(
                moc_record["hira_entries"],
                key=lambda x: x.get("hira_id") or 0
            )

        # ============================
        # Parse closure_data if stored as JSON string
        # ============================
        if "closure_data" in moc_record and moc_record["closure_data"]:
            if isinstance(moc_record["closure_data"], str):
                try:
                    moc_record["closure_data"] = json.loads(moc_record["closure_data"])
                except json.JSONDecodeError:
                    moc_record["closure_data"] = {}
            # Extract closure_date and closure_comments from closure_data
            if isinstance(moc_record["closure_data"], dict):
                moc_record["closure_date"] = moc_record["closure_data"].get("job_completion_date")
                moc_record["closure_comments"] = moc_record["closure_data"].get("comments_initiator")
        else:
            moc_record["closure_data"] = {}

        # ============================
        # Helper: fetch designation by user_id
        # ============================
        def get_designation_by_id(user_id):
            if not user_id:
                return None
            row = db.execute(
                text("SELECT designation FROM users WHERE user_id = :uid"),
                {"uid": user_id}
            ).fetchone()
            return row.designation if row else None

        # ============================
        # Helper: fetch designation by full name or username
        # ============================
        def get_designation_by_name(name):
            if not name:
                return None
            row = db.execute(
                text("""
                    SELECT designation FROM users 
                    WHERE CONCAT(first_name, ' ', last_name) = :name
                    OR username = :name
                """),
                {"name": name}
            ).fetchone()
            return row.designation if row else None

        # ============================
        # Helper: fetch all reviewers by role_id=3 and submenu_id=2
        # ============================
        def get_reviewers():
            rows = db.execute(
                text("""
                    SELECT DISTINCT
                        u.user_id,
                        CONCAT(u.first_name, ' ', u.last_name) AS full_name,
                        u.designation
                    FROM role_permissions rp
                    JOIN users u ON u.user_id = rp.user_id
                    WHERE rp.role_id = 3
                    AND rp.submenu_id = 2
                    AND u.is_deleted = false
                """)
            ).fetchall()
            return [
                {
                    "reviewer_id": row.user_id,
                    "reviewer_name": row.full_name,
                    "reviewer_designation": row.designation
                }
                for row in rows
            ]

        # ============================
        # Helper: get correct SIC (role_id=2, submenu_id=2)
        # ============================
        def get_correct_sic(station_name):
            if not station_name:
                return None, None, None
            
            row = db.execute(
                text("""
                    SELECT 
                        rp.user_id,
                        CONCAT(u.first_name, ' ', u.last_name) AS full_name,
                        u.designation
                    FROM role_permissions rp
                    JOIN users u ON u.user_id = rp.user_id
                    JOIN station s ON s.station_id = u.station_id
                    WHERE rp.role_id = 2
                      AND rp.submenu_id = 2
                      AND LOWER(TRIM(s.station_name)) = LOWER(TRIM(:station_name))
                    LIMIT 1
                """),
                {"station_name": station_name}
            ).fetchone()
            
            if row:
                return row.user_id, row.full_name, row.designation
            return None, None, None

        # ============================
        # Enrich with designations
        # ============================
        moc_record["hira_reviewer_designation"] = get_designation_by_id(moc_record.get("hira_reviewer_id"))
        moc_record["approver_designation"] = get_designation_by_id(moc_record.get("approver_id"))
        moc_record["created_by_designation"] = get_designation_by_name(moc_record.get("created_by"))

        # ============================
        # Override SIC with correct lookup (role_id=2, submenu_id=2)
        # ============================
        sic_id, sic_name, sic_designation = get_correct_sic(moc_record.get("station_name"))

        if sic_id:
            moc_record["sic_id"] = sic_id
            moc_record["sic_name"] = sic_name
            moc_record["sic_designation"] = sic_designation
        else:
            # Fallback to original if no match found
            moc_record["sic_designation"] = get_designation_by_id(moc_record.get("sic_id"))

        # ============================
        # Enrich with all available reviewers
        # ============================
        moc_record["available_approver"] = get_reviewers()

        return MOCRequestDetail(**moc_record)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e





def get_moc_status_summary_by_user(db: Session, req: MOCStatusCountRequest):
    try:
        sql = text("""
            SELECT public.get_moc_status_summary_by_user(:user_id)
        """)
        result = db.execute(sql, {"user_id": req.user_id}).scalar_one_or_none()
        return result or {}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
def get_moc_status_summary_by_station(db: Session, req: MOCStatusCountRequestStation):
    try:
        sql = text("""
            SELECT 
                COUNT(*) AS total_requests,

                COUNT(*) FILTER (WHERE status = 'Approved') AS approved,
                COUNT(*) FILTER (WHERE status = 'Pending Review') AS pending_review,
                COUNT(*) FILTER (WHERE status = 'Pending HIRA Review') AS pending_hira_review,
                COUNT(*) FILTER (WHERE status = 'Closed') AS moc_closed,
                COUNT(*) FILTER (WHERE status = 'Rejected') AS rejected

            FROM moc_requests
            WHERE station_name = :station_name
        """)

        # ✅ FIX HERE
        result = db.execute(sql, {
            "station_name": req.station_name
        }).mappings().one()

        return {
            "role_id": 1,
            "total_requests": result["total_requests"] or 0,
            "approved": result["approved"] or 0,
            "pending_review": result["pending_review"] or 0,
            "pending_hira_review": result["pending_hira_review"] or 0,
            "moc_closed": result["moc_closed"] or 0,
            "rejected": result["rejected"] or 0
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
from sqlalchemy import text

def get_all_station_summary(db: Session):
    try:
        sql = text("""
            SELECT 
                COUNT(*) AS total_requests,

                COUNT(*) FILTER (WHERE status = 'Approved') AS approved,
                COUNT(*) FILTER (WHERE status = 'Pending Review') AS pending_review,
                COUNT(*) FILTER (WHERE status = 'Pending HIRA Review') AS pending_hira_review,
                COUNT(*) FILTER (WHERE status = 'Closed') AS moc_closed,
                COUNT(*) FILTER (WHERE status = 'Rejected') AS rejected

            FROM moc_requests
        """)

        result = db.execute(sql).mappings().first()

        data = {
            "total_requests": result["total_requests"] or 0,
            "approved": result["approved"] or 0,
            "pending_review": result["pending_review"] or 0,
            "pending_hira_review": result["pending_hira_review"] or 0,
            "moc_closed": result["moc_closed"] or 0,
            "rejected": result["rejected"] or 0
        }

        return data

    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
       
def get_sic_approved_model(db: Session):
    try:
        sql = text("""
                SELECT public.get_sic_approved()
        """)
        result = db.execute(sql).scalar_one_or_none()
        return result or {}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

def get_hira_approved_model(db: Session):
    try:
        sql = text("""
                SELECT public.get_hira_approved()
        """)
        result = db.execute(sql).scalar_one_or_none()
        return result or {}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
def get_submitted_model(db: Session):
    try:
        sql = text("""
                SELECT public.get_submitted()
        """)
        result = db.execute(sql).scalar_one_or_none()
        return result or {}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
from sqlalchemy import text

def update_moc_request_service(db, request):
    try:
        update_query = text("""
    UPDATE public.moc_requests
    SET
        station_name = :station_name,
        title = :title,
        date = :date,
        priority = :priority,
        modification_type = :modification_type,
        time_limit = :time_limit,
        shutdown_required = :shutdown_required,
        present_system = :present_system,
        proposed_change = :proposed_change,
        justification = :justification,
        objectives = :objectives,
        other_units_impacted = :other_units_impacted,
        statutory_approval_required = :statutory_approval_required,
        statutory_approval_details = :statutory_approval_details,
        impact_of_modification = :impact_of_modification,
        consequences_non_implementation = :consequences_non_implementation,
        hse = :hse,
        efficiency = :efficiency,
        quality = :quality,
        reliability = :reliability,
        other_aspects_required = :other_aspects_required,
        other_aspects = :other_aspects,
        objectives_achieved = :objectives_achieved,
        attachments = :attachments,
        comments = :comments,
        short_text = :short_text,
        reviewer_comments = COALESCE(:reviewer_comments, reviewer_comments),
        approver_comments = COALESCE(:approver_comments, approver_comments),
        sic_comments      = COALESCE(:sic_comments, sic_comments),
        closure_comments = COALESCE(:closure_comments, closure_comments),

        submission_date    = COALESCE(:submission_date, submission_date),
        hira_approved_date = COALESCE(:hira_approved_date, hira_approved_date),
        sic_approved_date  = COALESCE(:sic_approved_date, sic_approved_date),
        approved_date      = COALESCE(:approved_date, approved_date),
        closure_date       = COALESCE(:closure_date, closure_date),

        status = :status,
        is_active = :is_active,
        updated_by = :updated_by,
        updated_at = NOW()
    WHERE moc_request_no = :moc_request_no
""")
        result = db.execute(update_query, vars(request))

        if result.rowcount == 0:
            db.rollback()
            return {"status": "error", "message": "MOC Request not found"}

        # 2️⃣ INSERT HISTORY SNAPSHOT
        history_query = text("""
            INSERT INTO public.moc_request_history (
                moc_request_no,
                station_name,
                title,
                date,
                priority,
                modification_type,
                time_limit,
                shutdown_required,
                present_system,
                proposed_change,
                justification,
                objectives,
                other_units_impacted,
                statutory_approval_required,
                statutory_approval_details,
                impact_of_modification,
                consequences_non_implementation,
                hse,
                efficiency,
                quality,
                reliability,
                other_aspects_required,
                other_aspects,
                objectives_achieved,
                attachments,
                comments,
                short_text,
                reviewer_comments,
                approver_comments,
                sic_comments,
                status,
                is_active,
                submission_date,
                hira_approved_date,
                sic_approved_date,
                approved_date,
                closure_date,
                closure_comments,
                created_by,
                updated_by,
                created_at,
                updated_at
            )
            SELECT
                moc_request_no,
                station_name,
                title,
                date,
                priority,
                modification_type,
                time_limit,
                shutdown_required,
                present_system,
                proposed_change,
                justification,
                objectives,
                other_units_impacted,
                statutory_approval_required,
                statutory_approval_details,
                impact_of_modification,
                consequences_non_implementation,
                hse,
                efficiency,
                quality,
                reliability,
                other_aspects_required,
                other_aspects,
                objectives_achieved,
                attachments,
                comments,
                short_text,
                reviewer_comments,
                approver_comments,
                sic_comments,
                status,
                is_active,
                submission_date,
                hira_approved_date,
                sic_approved_date,
                approved_date,
                closure_date,
                closure_comments,
                updated_by,
                updated_by,
                NOW(),
                NOW()
            FROM public.moc_requests
            WHERE moc_request_no = :p_moc_request_no
        """)

        db.execute(history_query, {"p_moc_request_no": request.moc_request_no})

        db.commit()
        return {"status": "success", "message": "MOC updated successfully"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}





def get_all_engineer_details(db, user_id: int):
    try:
        query = text(f"SELECT * FROM public.get_all_engineer_details(:user_id)")
        result = db.execute(query, {"user_id": user_id}).fetchall()

        data = [
            {
                "user_id": row.user_id,
                "username": row.username,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "contact_phone": row.contact_phone,
                "role_name": row.role_name
            }
            for row in result
        ]

        return {
            "statusCode": "0000",
            "statusMessage": "Success",
            "data": data
        }

    except Exception as e:
        return {
            "statusCode": "9999",
            "statusMessage": f"Error while fetching engineer details: {str(e)}",
            "data": []
        }
    



def get_moc_requests_by_user(db, user_id: int):
    try:
        query = text("SELECT * FROM public.get_moc_requests_by_user(:user_id)")
        result = db.execute(query, {"user_id": user_id}).fetchall()

        data = [dict(row._mapping) for row in result]

        # ============================
        # Fetch all available reviewers (role_id=3, submenu_id=2)
        # ============================
        reviewer_rows = db.execute(
            text("""
                SELECT DISTINCT
                    u.user_id,
                    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
                    u.designation
                FROM role_permissions rp
                JOIN users u ON u.user_id = rp.user_id
                WHERE rp.role_id = 3
                AND rp.submenu_id = 2
                AND u.is_deleted = false
            """)
        ).fetchall()
        available_reviewers = [
            {
                "reviewer_id": row.user_id,
                "reviewer_name": row.full_name,
                "reviewer_designation": row.designation
            }
            for row in reviewer_rows
        ]
        sic_rows = db.execute(
            text("""
                SELECT DISTINCT
                    u.user_id,
                    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
                    u.designation
                FROM role_permissions rp
                JOIN users u ON u.user_id = rp.user_id
                WHERE rp.role_id = 2
                AND rp.submenu_id = 2
                AND u.is_deleted = false
            """)
        ).fetchall()
        available_sic = [
            {
                "sic_id": row.user_id,
                "sic_name": row.full_name,
                "sic_designation": row.designation
            }
            for row in sic_rows
        ]

        return {
            "statusCode": "0000",
            "statusMessage": "Success",
            "data": data,
            "available_sic": available_sic,
            "available_reviewers": available_reviewers
        }

    except Exception as e:
        return {
            "statusCode": "9999",
            "statusMessage": f"Error: {str(e)}",
            "data": [],
            "available_sic": [],
            "available_reviewers": []
        }







