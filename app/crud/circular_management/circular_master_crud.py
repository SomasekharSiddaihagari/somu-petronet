from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import UploadFile
import os
import uuid
import json  

from app.routers.UserAuthR2 import make_download_url
from app.routers.travel_expense.travel_daily_router import delete_da
from app.schemas.circular_management.circular_master_schema import (
    CircularCreate,
    CircularUpdate
)

# -------------------------------------------------
# CREATE (MASTER + HISTORY – MULTI FILE SAFE)
# -------------------------------------------------
UPLOAD_DIR = "uploads/circulars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# def get_next_doc_seq(db: Session, category_id: int, subcategory_id, cat_name: str, sub_name: str) -> str:
#     """
#     Returns the next zero-padded sequence string (e.g. '003') for the given
#     category/sub_category combination by inspecting the MAX number already
#     stored in document_no across both circular_master and circular_master_history.
#     Format stored: CLR/<cat>/<sub>/<seq>   or   CLR/<cat>/<seq>
#     """
#     prefix = f"CLR/{cat_name}/{sub_name}/" if sub_name else f"CLR/{cat_name}/"

#     # Query max sequence from both live and history tables
#     max_seq_sql = text("""
#         SELECT COALESCE(MAX(
#             CAST(
#                 CASE
#                     WHEN document_no LIKE :prefix || '%'
#                     THEN SPLIT_PART(SUBSTRING(document_no FROM LENGTH(:prefix) + 1), '/', 1)
#                     ELSE '0'
#                 END AS INTEGER
#             )
#         ), 0)
#         FROM (
#             SELECT document_no FROM circular_master
#             WHERE category_id = :cat
#             AND ((:sub IS NULL AND subcategory_id IS NULL) OR subcategory_id = :sub)
#             UNION ALL
#             SELECT document_no FROM circular_master_history
#             WHERE category_id = :cat
#             AND ((:sub IS NULL AND subcategory_id IS NULL) OR subcategory_id = :sub)
#         ) AS all_docs
#         WHERE document_no LIKE :prefix || '%'
#     """)

#     max_seq = db.execute(max_seq_sql, {
#         "prefix": prefix,
#         "cat": category_id,
#         "sub": subcategory_id
#     }).scalar() or 0

#     return str(max_seq + 1).zfill(3)

def create_circular(
    db: Session,
    payload: dict,
    target_audience: list,
    files: list[UploadFile]
):   
    names = db.execute(text("""
        SELECT
            c.category_name,
            s.subcategory_name
        FROM category_master c
        LEFT JOIN subcategory_master s ON s.subcategory_id = :sub
        WHERE c.category_id = :cat
    """), {"cat": payload["category_id"], "sub": payload.get("subcategory_id")}).mappings().first()

    cat_name = names["category_name"] if names and names["category_name"] else "Unknown"
    sub_name = names["subcategory_name"] if names and names["subcategory_name"] else ""

    # seq_str = get_next_doc_seq(db, payload["category_id"], payload.get("subcategory_id"), cat_name, sub_name)
    # Every new POST always starts with 001
    seq_str = "001"
    if sub_name:
        payload["document_no"] = f"CLR/{cat_name}/{sub_name}/{seq_str}"
    else:
        payload["document_no"] = f"CLR/{cat_name}/{seq_str}"

    # if payload.get("subcategory_id"):
    #     seq_query = text("SELECT COUNT(*) FROM circular_master WHERE category_id = :cat AND subcategory_id = :sub")
    # else:
    #     seq_query = text("SELECT COUNT(*) FROM circular_master WHERE category_id = :cat AND subcategory_id IS NULL")
        
    # count = db.execute(seq_query, {"cat": payload["category_id"], "sub": payload.get("subcategory_id")}).scalar() or 0
    # seq_str = str(count + 1).zfill(3)
    # change_type_str = payload.get("change_type", "1.0")

    # if sub_name:
    #     payload["document_no"] = f"CLR/{cat_name}/{sub_name}/{seq_str}/{change_type_str}"
    # else:
    #     payload["document_no"] = f"CLR/{cat_name}/{seq_str}/{change_type_str}"

    
    
    # ---------------- MASTER ----------------
    insert_master = text("""
        INSERT INTO circular_master (
            title, category_id, subcategory_id, content,
            change_type, mandatory_status, status,
            created_by, created_date,tags, document_no
        )
        VALUES (
            :title, :category_id, :subcategory_id, :content,
            :change_type, :mandatory_status, :status,
            :created_by, NOW(),:tags, :document_no
        )
        RETURNING circular_id
    """)

    # ---------------- MASTER HISTORY ----------------
    insert_master_history = text("""
        INSERT INTO circular_master_history (
            circular_id, title, category_id, subcategory_id,
            content, change_type, mandatory_status, status,
            is_deleted, is_archived, read_count, acknowledge_count,
            created_by, created_date, updated_by, updated_date,tags, document_no
        )
        SELECT
            circular_id, title, category_id, subcategory_id,
            content, change_type, mandatory_status, status,
            is_deleted, is_archived, read_count, acknowledge_count,
            created_by, created_date, updated_by, updated_date,tags, document_no
        FROM circular_master
        WHERE circular_id = :circular_id
    """)
    # ---------------- TARGET ----------------      
    insert_target = text("""
        INSERT INTO circular_target_audience (
            circular_id, audience_type, audience_ref_id,
            created_by, created_date, version
        )
        VALUES (
            :circular_id, :audience_type,
            CAST(:audience_ref_id AS jsonb),
            :created_by, NOW(), :version
        )
        RETURNING audience_id
    """)

    insert_target_history = text("""
        INSERT INTO circular_target_audience_history (
            circular_id, audience_type, audience_ref_id,
            created_by, created_date,
            updated_by, updated_date,version
        )
        SELECT
            circular_id, audience_type, audience_ref_id,
            created_by, created_date,
            updated_by, updated_date,version
        FROM circular_target_audience
        WHERE audience_id = :audience_id
    """)

    # ---------------- ATTACHMENTS ----------------
    insert_attachment = text("""
        INSERT INTO circular_attachments (
            circular_id, file_name, file_path,
            file_type, file_size,
            uploaded_by, uploaded_at,version
        )
        VALUES (
            :circular_id, :file_name, :file_path,
            :file_type, :file_size,
            :uploaded_by, NOW(),:version
        )
        RETURNING attachment_id
    """)

    insert_attachment_history = text("""
        INSERT INTO circular_attachments_history (
            attachment_id, circular_id, file_name, file_path,
            file_type, file_size, uploaded_by, uploaded_at,version
        )
        SELECT
            attachment_id, circular_id, file_name, file_path,
            file_type, file_size, uploaded_by, uploaded_at,version
        FROM circular_attachments
        WHERE attachment_id = :attachment_id
    """)

    try:
        # ---------------- MASTER ----------------
        circular_id = db.execute(insert_master, payload).scalar()

        # ---------------- MASTER HISTORY ----------------
        db.execute(insert_master_history, {"circular_id": circular_id})

        # ---------------- TARGET AUDIENCE + HISTORY ----------------
        for ta in target_audience:
            audience_id = db.execute(
                insert_target,
                {
                    "circular_id": circular_id,
                    "audience_type": ta["audience_type"],
                    "audience_ref_id": json.dumps(ta["audience_ref_id"]),
                    "created_by": payload["created_by"],
                    "version": payload["change_type"]
                }
            ).scalar()

            db.execute(insert_target_history, {"audience_id": audience_id})

        # ---------------- ATTACHMENTS + HISTORY ----------------
        for file in files or []:
            if not file.filename:
                continue

            unique_name = f"{circular_id}_{uuid.uuid4().hex}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, unique_name)

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            attachment_id = db.execute(
                insert_attachment,
                {
                    "circular_id": circular_id,
                    "file_name": file.filename,
                    "file_path": file_path,
                    "file_type": file.content_type,
                    "file_size": file.size,
                    "uploaded_by": payload["created_by"],
                    "version": payload["change_type"]
                }
            ).scalar()

            db.execute(insert_attachment_history, {"attachment_id": attachment_id})

        db.commit()

        return {"message": "Circular created successfully", "circular_id": circular_id}

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create circular: {str(e)}")


# -------------------------------------------------
# UPDATE (MASTER + HISTORY – EXACT SNAPSHOT)
# -------------------------------------------------
def update_circular(
    db: Session,
    circular_id: int,
    payload: dict,
    target_audience: list,
    files: list[UploadFile]
):
    old_master = db.execute(text("""
        SELECT document_no, category_id, subcategory_id
        FROM circular_master
        WHERE circular_id = :circular_id
    """), {"circular_id": circular_id}).mappings().first()
    if not old_master:
        return None
    
    old_cat = old_master["category_id"]
    old_sub = old_master["subcategory_id"]
    old_doc_no = old_master["document_no"] or ""

    new_cat = payload.get("category_id") if payload.get("category_id") is not None else old_cat
    new_sub = payload.get("subcategory_id") if "subcategory_id" in payload else old_sub

    payload["category_id"] = new_cat
    payload["subcategory_id"] = new_sub

    names = db.execute(text("""
        SELECT
            (SELECT category_name FROM category_master WHERE category_id = :cat) as cat_name,
            (SELECT subcategory_name FROM subcategory_master WHERE subcategory_id = :sub) as sub_name
    """), {"cat": new_cat, "sub": new_sub}).mappings().first()

    cat_name = names["cat_name"] if names and names["cat_name"] else "Unknown"
    sub_name = names["sub_name"] if names and names["sub_name"] else ""
    # change_type_str = payload.get("change_type") if payload.get("change_type") else "1.0"

    # if new_cat != old_cat or new_sub != old_sub:
    #     if new_sub:
    #         seq_query = text("SELECT COUNT(*) FROM circular_master WHERE category_id = :cat AND subcategory_id = :sub")
    #     else:
    #         seq_query = text("SELECT COUNT(*) FROM circular_master WHERE category_id = :cat AND subcategory_id IS NULL")
    #     count = db.execute(seq_query, {"cat": new_cat, "sub": new_sub}).scalar() or 0
    #     seq_str = str(count + 1).zfill(3)
    # else:
    #     parts = old_doc_no.split("/")
    #     if len(parts) >= 4:
    #         seq_str = parts[-2]
    #     else:
    #         seq_str = "001"
    # seq_str = get_next_doc_seq(db, new_cat, new_sub, cat_name, sub_name)
        # Logic for Incrementing or Resetting sequence
    if new_cat == old_cat and new_sub == old_sub:
        # Same category/sub-category: Increment the sequence from the old document_no
        try:
            parts = old_doc_no.split('/')
            last_part = parts[-1]
            # Handle potential suffixes like -R1 if they exist, otherwise just cast to int
            current_seq = int(last_part.split('-')[0]) 
            seq_str = str(current_seq + 1).zfill(3)
        except (ValueError, IndexError, AttributeError):
            seq_str = "001" # Fallback if format is broken
    else:
        # Category or Sub-category changed: Reset to 001
        seq_str = "001"

    if sub_name:
        # payload["document_no"] = f"CLR/{cat_name}/{sub_name}/{seq_str}/{change_type_str}"
        payload["document_no"] = f"CLR/{cat_name}/{sub_name}/{seq_str}"

    else:
        # payload["document_no"] = f"CLR/{cat_name}/{seq_str}/{change_type_str}"
        payload["document_no"] = f"CLR/{cat_name}/{seq_str}"


    # ---------------- MASTER UPDATE ----------------
    update_master = text("""
        UPDATE circular_master
        SET
            title = COALESCE(:title, title),
            category_id =:category_id,
            subcategory_id =:subcategory_id,
            content = COALESCE(:content, content),
            change_type = COALESCE(:change_type, change_type),
            mandatory_status = COALESCE(:mandatory_status, mandatory_status),
            status = COALESCE(:status, status),
            updated_by = :updated_by,
            updated_date = NOW(),
            tags = COALESCE(:tags, tags),
            reason = COALESCE(:reason, reason),
            document_no =:document_no
        WHERE circular_id = :circular_id
    """)

    update_masters = text("""
        UPDATE circular_user_activity
        SET
            is_read = NULL,
            is_acknowledged = NULL,
            acknowledged_at = NULL,
            read_at = NULL
        WHERE circular_id = :circular_id
    """)

    

    # ---------------- MASTER HISTORY ----------------
    insert_master_history = text("""
        INSERT INTO circular_master_history (
            circular_id, title, category_id, subcategory_id,
            content, change_type, mandatory_status, status,
            is_deleted, is_archived, read_count, acknowledge_count,
            created_by, created_date, updated_by, updated_date, tags, reason,document_no
        )
        SELECT
            circular_id, title, category_id, subcategory_id,
            content, change_type, mandatory_status, status,
            is_deleted, is_archived, read_count, acknowledge_count,
            created_by, created_date, updated_by, updated_date, tags, reason, document_no
        FROM circular_master
        WHERE circular_id = :circular_id
    """)

    # ---------------- TARGET UPSERT ----------------
    upsert_target = text("""
        INSERT INTO circular_target_audience (
            circular_id,
            audience_type,
            audience_ref_id,
            created_by,
            created_date,
            updated_by,
            updated_date,
            version
        )
        VALUES (
            :circular_id,
            :audience_type,
            CAST(:audience_ref_id AS jsonb),
            :updated_by,
            NOW(),
            :updated_by,
            NOW(),
            :version
        )
        ON CONFLICT (circular_id, audience_type)
        DO UPDATE SET
            audience_ref_id = EXCLUDED.audience_ref_id,
            updated_by = EXCLUDED.updated_by,
            updated_date = NOW(),
            version = EXCLUDED.version
    """)

    # ---------------- ATTACHMENT HISTORY ----------------
    insert_attachment_history = text("""
        INSERT INTO circular_attachments_history (
            attachment_id, circular_id, file_name, file_path,
            file_type, file_size, uploaded_by, uploaded_at, version
        )
        SELECT
            ca.attachment_id, ca.circular_id, ca.file_name, ca.file_path,
            ca.file_type, ca.file_size, ca.uploaded_by, ca.uploaded_at, ca.version
        FROM circular_attachments ca
        WHERE ca.circular_id = :circular_id
    """)

    delete_attachments = text("""
        DELETE FROM circular_attachments
        WHERE circular_id = :circular_id
    """)

    insert_attachment = text("""
        INSERT INTO circular_attachments (
            circular_id, file_name, file_path,
            file_type, file_size, uploaded_by, uploaded_at, version
        )
        VALUES (
            :circular_id, :file_name, :file_path,
            :file_type, :file_size, :uploaded_by, NOW(), :version
        )
    """)

    try:
        # =================================================
        # 1️⃣ UPDATE MASTER
        # =================================================
        payload["circular_id"] = circular_id
        db.execute(update_master, payload)
        db.execute(update_masters, {"circular_id": circular_id})

        # =================================================
        # 2️⃣ MASTER HISTORY
        # =================================================
        db.execute(insert_master_history, {"circular_id": circular_id})

        # =================================================
        # 3️⃣ TARGET AUDIENCE LOGIC (FIXED 🔥)
        # =================================================
        for ta in target_audience:

            removed_users = ta.get("removed_users", [])

    # -------------------------------------------------
    # 1️⃣ UPDATE PREVIOUS HISTORY
    # -------------------------------------------------
            if removed_users:
                db.execute(text("""
                    UPDATE circular_target_audience_history
                    SET removed_user = CAST(:removed_users AS jsonb)
                    WHERE history_id = (
                        SELECT history_id
                        FROM circular_target_audience_history
                        WHERE circular_id = :circular_id
                        AND audience_type = :audience_type
                        ORDER BY updated_date DESC NULLS LAST, history_id DESC
                        LIMIT 1
                    )
                """), {
                    "circular_id": circular_id,
                    "audience_type": ta["audience_type"],
                    "removed_users": json.dumps(removed_users)
                })

            # -------------------------------------------------
            # 2️⃣ UPDATE CURRENT TABLE FIRST ✅
            # -------------------------------------------------
            db.execute(
                    upsert_target,
                    {
                        "circular_id": circular_id,
                        "audience_type": ta["audience_type"],
                        "audience_ref_id": json.dumps(ta["audience_ref_id"]),
                        "updated_by": payload["updated_by"],
                        "version": payload["change_type"]
                    }
                )

            # -------------------------------------------------
            # 3️⃣ INSERT HISTORY (NOW GETS NEW DATA ✅)
            # -------------------------------------------------
            db.execute(text("""
                        INSERT INTO circular_target_audience_history (
                        circular_id,
                        audience_type,
                        audience_ref_id,
                        created_by,
                        created_date,
                        updated_by,
                        updated_date,
                        version,
                        removed_user
                    )
                    SELECT
                        circular_id,
                        audience_type,
                        audience_ref_id,
                        created_by,
                        created_date,
                        :updated_by,
                        NOW(),
                        :version,
                        NULL
                    FROM circular_target_audience
                    WHERE circular_id = :circular_id
                    AND audience_type = :audience_type
                """), {
                    "circular_id": circular_id,
                    "audience_type": ta["audience_type"],
                    "updated_by": payload["updated_by"],
                    "version": payload["change_type"]
                })

        # =================================================
        # 4️⃣ ATTACHMENTS
        # =================================================
        if files:
            db.execute(insert_attachment_history, {"circular_id": circular_id})
            db.execute(delete_attachments, {"circular_id": circular_id})

            os.makedirs(UPLOAD_DIR, exist_ok=True)

            for file in files:
                file_path = f"{UPLOAD_DIR}/{circular_id}_{file.filename}"

                with open(file_path, "wb") as f:
                    f.write(file.file.read())

                db.execute(
                    insert_attachment,
                    {
                        "circular_id": circular_id,
                        "file_name": file.filename,
                        "file_path": file_path,
                        "file_type": file.content_type,
                        "file_size": file.size,
                        "uploaded_by": payload["updated_by"],
                        "version": payload["change_type"]
                    }
                )

        db.commit()

        return {
            "message": "Circular updated successfully",
            "circular_id": circular_id
        }

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update circular: {str(e)}")

# -------------------------------------------------
# GET BY ID (JSONB audience split & merged)
# -------------------------------------------------
def get_circular(db: Session, circular_id: int, version: str):

    # -------------------------------------------------
    # 1️⃣ CHECK CURRENT TABLE
    # -------------------------------------------------
    check_query = text("""
        SELECT 1
        FROM circular_master
        WHERE circular_id = :circular_id
        AND change_type = :version
        AND is_deleted = FALSE
    """)

    exists = db.execute(
        check_query,
        {"circular_id": circular_id, "version": version}
    ).scalar()

    # -------------------------------------------------
    # 2️⃣ DYNAMIC TABLE SELECTION
    # -------------------------------------------------
    if exists:
        master_table = "circular_master"
        target_table = "circular_target_audience"
        attachment_table = "circular_attachments"
    else:
        master_table = "circular_master_history"
        target_table = "circular_target_audience_history"
        attachment_table = "circular_attachments_history"

    # -------------------------------------------------
    # 3️⃣ MAIN QUERY
    # -------------------------------------------------
    query = text(f"""
        WITH audience_expanded AS (
            SELECT
                cta.circular_id,
                cta.audience_type,
                jsonb_array_elements_text(cta.audience_ref_id)::INT AS ref_id
            FROM {target_table} cta
            WHERE cta.circular_id = :circular_id
              AND cta.version = :version
        )

        SELECT
            cm.circular_id,
            cm.document_no,
            cm.title,
            cm.content,
            cm.category_id,
            cat.category_name,
            cm.subcategory_id,
            sub.subcategory_name,
            cm.change_type,
            cm.mandatory_status,
            cm.status,
            cm.read_count,
            cm.acknowledge_count,
            cm.created_by,
            creator.username as created_name,
            creator.first_name,
            creator.last_name,
            cm.created_date,
            cm.updated_by,
            cm.updated_date,
            cm.tags,
            ae.audience_type,

            -- GROUP
            gm.group_id,
            gm.group_name,

            -- STATION
            sm.station_id,
            sm.station_name,

            -- INDIVIDUAL
            u.user_id,
            u.username

        FROM {master_table} cm

        JOIN category_master cat
            ON cm.category_id = cat.category_id

        LEFT JOIN subcategory_master sub
            ON cm.subcategory_id = sub.subcategory_id

        LEFT JOIN users creator
            ON cm.created_by = creator.user_id

        LEFT JOIN audience_expanded ae
            ON ae.circular_id = cm.circular_id

        LEFT JOIN group_master gm
            ON ae.audience_type = 'GROUP'
           AND gm.group_id = ae.ref_id

        LEFT JOIN station sm
            ON ae.audience_type = 'STATION'
           AND sm.station_id = ae.ref_id

        LEFT JOIN users u
            ON ae.audience_type = 'INDIVIDUAL'
           AND u.user_id = ae.ref_id

        WHERE cm.circular_id = :circular_id
          AND cm.change_type = :version
    """)

    rows = db.execute(
        query,
        {"circular_id": circular_id, "version": version}
    ).mappings().all()

    if not rows:
        return None

    # -------------------------------------------------
    # 4️⃣ BASE DATA
    # -------------------------------------------------
    base = dict(rows[0])

    # -------------------------------------------------
    # 5️⃣ TARGET AUDIENCE FORMAT
    # -------------------------------------------------
    audience = {}

    for row in rows:
        atype = row["audience_type"]
        if not atype:
            continue

        audience.setdefault(atype, [])

        if atype == "GROUP" and row["group_id"]:
            audience[atype].append({
                "group_id": row["group_id"],
                "group_name": row["group_name"]
            })

        elif atype == "STATION" and row["station_id"]:
            audience[atype].append({
                "station_id": row["station_id"],
                "station_name": row["station_name"]
            })

        elif atype == "INDIVIDUAL" and row["user_id"]:
            audience[atype].append({
                "user_id": row["user_id"],
                "username": row["username"]
            })

    base["target_audience"] = audience

    # -------------------------------------------------
    # 6️⃣ ATTACHMENTS
    # -------------------------------------------------
    attachment_query = text(f"""
        SELECT Distinct ON (attachment_id) attachment_id,
            file_name,
            file_path,
            file_type,
            file_size,
            uploaded_by,
            uploaded_at
        FROM {attachment_table}
        WHERE circular_id = :circular_id
          AND version = :version
        ORDER BY attachment_id, uploaded_at DESC
    """)

    attachments = db.execute(
        attachment_query,
        {"circular_id": circular_id, "version": version}
    ).mappings().all()

    formatted_attachments = []

    for att in attachments:
        att_dict = dict(att)
        att_dict["file_path"] = make_download_url(att_dict["file_path"])
        formatted_attachments.append(att_dict)

    base["attachments"] = formatted_attachments

    # -------------------------------------------------
    # 7️⃣ CLEANUP
    # -------------------------------------------------
    for key in [
        "audience_type",
        "group_id", "group_name",
        "station_id", "station_name",
        "user_id", "username"
    ]:
        base.pop(key, None)

    return base


# -------------------------------------------------
# GET ALL ADMIN / PUBLISHER 
# -------------------------------------------------

def get_all_circulars(db: Session, user_id: int):

    query = text("""
        SELECT
            cm.circular_id,
            cm.document_no,
            cm.title,
            cm.category_id,
            cat.category_name,
            cm.subcategory_id,
            sub.subcategory_name,
            cm.content,
            cm.change_type,
            cm.mandatory_status,
            cm.status,
            cm.is_deleted,
            cm.is_archived,
            cm.read_count,
            cm.acknowledge_count,
            cm.created_by,
            usr.username AS created_by_name,
            cm.created_date,
            cm.updated_by,
            cm.updated_date,
            cm.tags,
            u.username AS updated_by_name
        FROM circular_master cm
        JOIN category_master cat
            ON cm.category_id = cat.category_id
        LEFT JOIN subcategory_master sub
            ON cm.subcategory_id = sub.subcategory_id
        LEFT JOIN users usr
            ON cm.created_by = usr.user_id
        LEFT JOIN users u
            ON cm.updated_by = u.user_id
        WHERE cm.is_deleted = FALSE
          AND cm.is_archived = FALSE
          AND cm.created_by = :user_id AND cm.is_archived= FALSE
        ORDER BY cm.circular_id DESC
    """)

    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().all()

# def get_all_circulars(db: Session, user_id: int):
#     # Check user role
#     role_query = text("""
#         SELECT r.role_name
#         FROM roles AS r
#         JOIN role_permissions AS rp ON r.role_id = rp.role_id
#         WHERE user_id = :user_id
#     """)

#     role = db.execute(
#         role_query,
#         {"user_id": user_id}
#     ).scalar()

#     # Base query
#     base_query = """
#         SELECT
#             cm.circular_id,
#             cm.title,
#             cm.category_id,
#             cat.category_name,
#             cm.subcategory_id,
#             sub.subcategory_name,
#             cm.content,
#             cm.change_type,
#             cm.mandatory_status,
#             cm.status,
#             cm.is_deleted,
#             cm.is_archived,
#             cm.read_count,
#             cm.acknowledge_count,
#             cm.created_by,
#             usr.username AS created_by_name,
#             cm.created_date,
#             cm.updated_by,
#             cm.tags,
#             u.username AS updated_by_name
#         FROM circular_master cm
#         JOIN category_master cat
#             ON cm.category_id = cat.category_id
#         JOIN subcategory_master sub
#             ON cm.subcategory_id = sub.subcategory_id
#         LEFT JOIN users usr
#             ON cm.created_by = usr.user_id
#         LEFT JOIN users u
#             ON cm.updated_by = u.user_id
#         WHERE cm.is_deleted = FALSE AND cm.is_archived = FALSE
#     """

#     params = {}

#     # 🔐 Non-admin users see only their data
#     if role != "Admin":
#         base_query += " AND cm.created_by = :user_id"
#         params["user_id"] = user_id

#     base_query += " ORDER BY cm.circular_id DESC"

#     query = text(base_query)
#     return db.execute(query, params).mappings().all()


# -------------------------------------------------
# GET COUNT OF THE CIRCULAR DASHBOARD
# -------------------------------------------------
def get_circular_dashboard_counts_crud(db: Session, user_id: int):
    # =========================
    # 🔹 GET ROLE
    # =========================
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    role = db.execute(role_query, {"user_id": user_id}).scalar()

    params = {"user_id": user_id}

    publisher_status = text("""
        SELECT p.status
        FROM publisher_master p
        WHERE p.user_id = :user_id
    """)

    pu_status = db.execute(publisher_status, {"user_id": user_id}).scalar()

    params = {"user_id": user_id}

    # =========================
    # ✅ ADMIN LOGIC (WORKING QUERY)
    # =========================
    if role and role.lower() in ["admin", "md"]:
        if pu_status and role and role.lower() == 'md' and pu_status.lower() == 'active':
            dashboard_query = text("""
            WITH audience_expanded AS (
                SELECT
                    cta.circular_id,
                    cta.audience_type,
                    jsonb_array_elements_text(cta.audience_ref_id)::INT AS ref_id
                FROM circular_target_audience cta
            )

            SELECT
                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND (
                        cm.created_by = :user_id

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'INDIVIDUAL'
                            AND ae.ref_id = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            JOIN group_master gm ON gm.group_id = ae.ref_id,
                                 jsonb_array_elements_text(gm.employee_ids) emp_id
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'GROUP'
                            AND emp_id::INT = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'STATION'
                            AND ae.ref_id = (
                                SELECT station_id
                                FROM users
                                WHERE user_id = :user_id
                            )
                        )
                    )
                ) AS total_circulars,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND DATE_TRUNC('month', cm.created_date)
                        = DATE_TRUNC('month', CURRENT_DATE)
                    AND (
                       

                         EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'INDIVIDUAL'
                            AND ae.ref_id = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            JOIN group_master gm ON gm.group_id = ae.ref_id,
                                 jsonb_array_elements_text(gm.employee_ids) emp_id
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'GROUP'
                            AND emp_id::INT = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'STATION'
                            AND ae.ref_id = (
                                SELECT station_id
                                FROM users
                                WHERE user_id = :user_id
                            )
                        )
                    )
                ) AS published_this_month,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND cm.created_by = :user_id
                ) AS my_published,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.is_archived = TRUE
                    AND cm.created_by = :user_id
                ) AS archived_count

            FROM circular_master cm
            WHERE cm.is_deleted = FALSE
        """)
        else:
            dashboard_query = text("""
            SELECT
                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                ) AS total_circulars,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND DATE_TRUNC('month', cm.created_date)
                        = DATE_TRUNC('month', CURRENT_DATE)
                ) AS published_this_month,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND cm.created_by = :user_id
                ) AS my_published,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.is_archived = TRUE
                    AND cm.created_by = :user_id
                ) AS archived_count

            FROM circular_master cm
            WHERE cm.is_deleted = FALSE
        """)

    # =========================
    # ✅ PUBLISHER / USER LOGIC
    # =========================
    else:

        dashboard_query = text("""
            WITH audience_expanded AS (
                SELECT
                    cta.circular_id,
                    cta.audience_type,
                    jsonb_array_elements_text(cta.audience_ref_id)::INT AS ref_id
                FROM circular_target_audience cta
            )

            SELECT
                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND (
                        cm.created_by = :user_id

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'INDIVIDUAL'
                            AND ae.ref_id = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            JOIN group_master gm ON gm.group_id = ae.ref_id,
                                 jsonb_array_elements_text(gm.employee_ids) emp_id
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'GROUP'
                            AND emp_id::INT = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'STATION'
                            AND ae.ref_id = (
                                SELECT station_id
                                FROM users
                                WHERE user_id = :user_id
                            )
                        )
                    )
                ) AS total_circulars,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND DATE_TRUNC('month', cm.created_date)
                        = DATE_TRUNC('month', CURRENT_DATE)
                    AND (
                       

                         EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'INDIVIDUAL'
                            AND ae.ref_id = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            JOIN group_master gm ON gm.group_id = ae.ref_id,
                                 jsonb_array_elements_text(gm.employee_ids) emp_id
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'GROUP'
                            AND emp_id::INT = :user_id
                        )

                        OR EXISTS (
                            SELECT 1
                            FROM audience_expanded ae
                            WHERE ae.circular_id = cm.circular_id
                            AND ae.audience_type = 'STATION'
                            AND ae.ref_id = (
                                SELECT station_id
                                FROM users
                                WHERE user_id = :user_id
                            )
                        )
                    )
                ) AS published_this_month,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.status = 'PUBLISHED'
                    AND cm.is_archived = FALSE
                    AND cm.created_by = :user_id
                ) AS my_published,

                COUNT(DISTINCT cm.circular_id)
                FILTER (
                    WHERE cm.is_archived = TRUE
                    AND cm.created_by = :user_id
                ) AS archived_count

            FROM circular_master cm
            WHERE cm.is_deleted = FALSE
        """)

    # =========================
    # 🔹 EXECUTE
    # =========================
    result = db.execute(dashboard_query, params).mappings().one()

    return {
        "total_circulars": result["total_circulars"],
        "published_this_month": result["published_this_month"],
        "my_published": result["my_published"],
        "archived": result["archived_count"]
    }


# -------------------------------------------------
# DELETE (SOFT DELETE + HISTORY)
# -------------------------------------------------
def delete_circular(db: Session, circular_id: int):
    update_query = text("""
        UPDATE circular_master
        SET
            is_deleted = TRUE,
        WHERE circular_id = :circular_id
          AND is_deleted = FALSE
    """)

    history_query = text("""
        INSERT INTO circular_master_history (
            circular_id,
            title,
            category_id,
            subcategory_id,
            content,
            change_type,
            mandatory_status,
            status,
            is_deleted,
            is_archived,
            read_count,
            acknowledge_count,
            created_by,
            created_date,
            updated_by,
            updated_date
        )
        SELECT
            circular_id,
            title,
            category_id,
            subcategory_id,
            content,
            change_type,
            mandatory_status,
            status,
            is_deleted,
            is_archived,
            read_count,
            acknowledge_count,
            created_by,
            created_date,
            updated_by,
            updated_date
        FROM circular_master
        WHERE circular_id = :circular_id
    """)

    try:
        result = db.execute(
            update_query,
            {
                "circular_id": circular_id,
                "deleted_by": delete_da
            }
        )

        if result.rowcount > 0:
            db.execute(history_query, {"circular_id": circular_id})

        db.commit()
        return result.rowcount

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to delete circular: {str(e)}")


# -------------------------------------------------
# GET ALL ARCHIVED CIRCULAR ADMIN / PUBLISHER
# -------------------------------------------------
def get_all_archived_circulars(db: Session, user_id: int):
    # Check user role
    role_query = text("""
        SELECT r.role_name
        FROM roles AS r
        JOIN role_permissions AS rp ON r.role_id = rp.role_id
        WHERE user_id = :user_id
    """)

    role = db.execute(
        role_query,
        {"user_id": user_id}
    ).scalar()

    publisher_status = text("""
        SELECT p.status
        FROM publisher_master p
        WHERE p.user_id = :user_id
    """)

    pu_status = db.execute(publisher_status, {"user_id": user_id}).scalar()

    params = {"user_id": user_id}

    # Base query
    base_query = """
        SELECT
            cm.circular_id,
            cm.document_no,
            cm.title,
            cm.category_id,
            cat.category_name,
            cm.subcategory_id,
            sub.subcategory_name,
            cm.content,
            cm.change_type,
            cm.mandatory_status,
            cm.status,
            cm.is_deleted,
            cm.is_archived,
            cm.read_count,
            cm.acknowledge_count,
            cm.created_by,
            usr.username AS created_by_name,
            cm.tags,
            cm.created_date,
            cm.updated_date,
            cm.updated_by,
            u.username AS updated_by_name
        FROM circular_master cm
        JOIN category_master cat
            ON cm.category_id = cat.category_id
        LEFT JOIN subcategory_master sub
            ON cm.subcategory_id = sub.subcategory_id
        LEFT JOIN users usr
            ON cm.created_by = usr.user_id
        LEFT JOIN users u
            ON cm.updated_by = u.user_id
        WHERE cm.is_deleted = FALSE
              AND cm.is_archived = TRUE
    """

    params = {}



    # 🔐 Non-admin users see only their data
    # if role != "Admin":
    if not (role and role.lower() in ["admin", "md"]):
        base_query += " AND cm.created_by = :user_id"
        params["user_id"] = user_id

    if pu_status and role and role.lower() == 'md' and pu_status.lower() == 'active':
        base_query += " AND cm.created_by = :user_id"
        params["user_id"] = user_id

    base_query += " ORDER BY cm.circular_id DESC"

    query = text(base_query)
    return db.execute(query, params).mappings().all()




# def get_all_archived_circulars(db: Session, user_id: int):
#     # Check user role
#     role_query = text("""
#         SELECT r.role_name
#         FROM roles AS r
#         JOIN role_permissions AS rp ON r.role_id = rp.role_id
#         WHERE user_id = :user_id
#     """)

#     role = db.execute(
#         role_query,
#         {"user_id": user_id}
#     ).scalar()

#     # Base query
#     base_query = """
#         SELECT
#             cm.circular_id,
#             cm.title,
#             cm.category_id,
#             cat.category_name,
#             cm.subcategory_id,
#             sub.subcategory_name,
#             cm.content,
#             cm.change_type,
#             cm.mandatory_status,
#             cm.status,
#             cm.is_deleted,
#             cm.is_archived,
#             cm.read_count,
#             cm.acknowledge_count,
#             cm.created_by,
#             usr.username AS created_by_name,
#             cm.created_date,
#             cm.updated_by,
#             u.username AS updated_by_name
#         FROM circular_master cm
#         JOIN category_master cat
#             ON cm.category_id = cat.category_id
#         JOIN subcategory_master sub
#             ON cm.subcategory_id = sub.subcategory_id
#         LEFT JOIN users usr
#             ON cm.created_by = usr.user_id
#         LEFT JOIN users u
#             ON cm.updated_by = u.user_id
#         WHERE cm.is_deleted = FALSE
#               AND cm.is_archived = TRUE
#     """

#     params = {}

#     # 🔐 Non-admin users see only their data
#     if role != "Admin":
#         base_query += " AND cm.created_by = :user_id"
#         params["user_id"] = user_id

#     base_query += " ORDER BY cm.circular_id DESC"

#     query = text(base_query)
#     return db.execute(query, params).mappings().all()


# -------------------------------------------------
# ARCHIVED CIRCULAR + HISTORY
# -------------------------------------------------
def archived_circular(db: Session, circular_id: int, status: bool):
    update_query = text("""
        UPDATE circular_master
        SET
            is_archived = :status
            WHERE circular_id = :circular_id
            AND is_deleted = FALSE
    """)

    history_query = text("""
        INSERT INTO circular_master_history (
            circular_id,
            title,
            category_id,
            subcategory_id,
            content,
            change_type,
            mandatory_status,
            status,
            is_deleted,
            is_archived,
            read_count,
            acknowledge_count,
            created_by,
            created_date,
            updated_by,
            updated_date
        )
        SELECT
            circular_id,
            title,
            category_id,
            subcategory_id,
            content,
            change_type,
            mandatory_status,
            status,
            is_deleted,
            is_archived,
            read_count,
            acknowledge_count,
            created_by,
            created_date,
            updated_by,
            updated_date
        FROM circular_master
        WHERE circular_id = :circular_id
    """)

    try:
        result = db.execute(
            update_query,
            {
                "circular_id": circular_id,
                "status": status,          # ✅ MUST include this

            }
        )

        if result.rowcount > 0:
            db.execute(history_query, {"circular_id": circular_id})

        db.commit()
        return result.rowcount

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to archived circular: {str(e)}")


# -------------------------------------------------
# GET ALL VERSION HISTORY (PURE HISTORY TABLES)
# -------------------------------------------------

def getall_version_history(db, circular_id: int, version: str):

     # -------------------------------------------------
    # 1️⃣ Get selected version date
    # -------------------------------------------------
    version_date_query = text("""
        SELECT COALESCE(updated_date, created_date) AS version_date
        FROM circular_master_history
        WHERE circular_id = :circular_id
          AND change_type = :version
        LIMIT 1
    """)

    version_date = db.execute(
        version_date_query,
        {"circular_id": circular_id, "version": version}
    ).scalar()

    if not version_date:
        return None

    # 1️⃣ Get all versions from master history
    master_query = text("""
        SELECT *
        FROM circular_master_history
        WHERE circular_id = :circular_id
          AND COALESCE(updated_date, created_date) <= :version_date
        ORDER BY created_date
    """)

    master_versions = db.execute(
        master_query,
        {"circular_id": circular_id,
         "version_date": version_date}
    ).mappings().all()

    if not master_versions:
        return None

    versions = []

    for mv in master_versions:

        version = mv["change_type"]  # This is your version (v1.0, v2.0 etc)

        # 2️⃣ Get Target Audience for this version
        audience_query = text("""
            WITH expanded AS (
                SELECT
                    cta.audience_type,
                    jsonb_array_elements_text(cta.audience_ref_id)::INT AS ref_id
                FROM circular_target_audience_history cta
                WHERE cta.circular_id = :circular_id
                  AND cta.version = :version
            )
            SELECT
                e.audience_type,
                gm.group_id,
                gm.group_name,
                sm.station_id,
                sm.station_name,
                u.user_id,
                u.username
            FROM expanded e
            LEFT JOIN group_master gm
                ON e.audience_type = 'GROUP'
               AND gm.group_id = e.ref_id
            LEFT JOIN station sm
                ON e.audience_type = 'STATION'
               AND sm.station_id = e.ref_id
            LEFT JOIN users u
                ON e.audience_type = 'INDIVIDUAL'
               AND u.user_id = e.ref_id
        """)

        audience_rows = db.execute(
            audience_query,
            {"circular_id": circular_id, "version": version}
        ).mappings().all()

        audience = {}

        for ar in audience_rows:
            atype = ar["audience_type"]
            audience.setdefault(atype, [])

            if atype == "GROUP" and ar["group_id"]:
                audience[atype].append({
                    "group_id": ar["group_id"],
                    "group_name": ar["group_name"]
                })

            elif atype == "STATION" and ar["station_id"]:
                audience[atype].append({
                    "station_id": ar["station_id"],
                    "station_name": ar["station_name"]
                })

            elif atype == "INDIVIDUAL" and ar["user_id"]:
                audience[atype].append({
                    "user_id": ar["user_id"],
                    "username": ar["username"]
                })

        # 3️⃣ Get Attachments for this version
        attachment_query = text("""
            SELECT *
            FROM circular_attachments_history
            WHERE circular_id = :circular_id
              AND version = :version
            ORDER BY uploaded_at
        """)

        attachment_rows = db.execute(
            attachment_query,
            {"circular_id": circular_id, "version": version}
        ).mappings().all()

        if not attachment_rows:
            attachment_query_main = text("""
                SELECT *
                FROM circular_attachments
                WHERE circular_id = :circular_id
                  AND version = :version
                ORDER BY uploaded_at
            """)

            attachment_rows = db.execute(
                attachment_query_main,
                {"circular_id": circular_id, "version": version}
            ).mappings().all()

        attachments = []

        for att in attachment_rows:
            attachments.append({
                "attachment_id": att["attachment_id"],
                "file_name": att["file_name"],
                "file_path": make_download_url(att["file_path"]),  # full URL
                "file_type": att["file_type"],
                "file_size": att["file_size"],
                "uploaded_by": att["uploaded_by"],
                "uploaded_at": att["uploaded_at"]
            })

        # 4️⃣ Append Version Object
        versions.append({
            "version": version,
            "version_date": mv["updated_date"] or mv["created_date"],
            "reason": mv.get("reason"),
            "content": mv.get("content"),
            "master_data": dict(mv),
            "target_audience": audience,
            "attachments": attachments
        })

    return {
        "circular_id": circular_id,
        "versions": versions
    }


# -------------------------------------------

#get api for displaying circulars in employee dashboard(getall circularsapi)
def get_employee_circulars(db: Session, user_id: int):

    # -------------------------------------------------
    # 1️⃣ Get User Role
    # -------------------------------------------------
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    role = db.execute(
        role_query,
        {"user_id": user_id}
    ).scalar()

    publisher_status = text("""
        SELECT p.status
        FROM publisher_master p
        WHERE p.user_id = :user_id
    """)

    pu_status = db.execute(publisher_status, {"user_id": user_id}).scalar()

    params = {"user_id": user_id}

    # -------------------------------------------------
    # 2️⃣ Base Query
    # -------------------------------------------------
    base_query = """
        SELECT DISTINCT
            c.circular_id,
            c.document_no,
            c.title,
            c.content,
            c.category_id,
            cat.category_name,
            c.subcategory_id,
            sub.subcategory_name,
            c.change_type AS version,
            c.mandatory_status,
            c.status,
            c.created_date AS published_date,
            c.created_by,
            c.updated_date,
            u.username AS publisher_name,
            c.tags,
            ua.is_read,
            CASE
    WHEN EXISTS (
        SELECT 1
        FROM circular_target_audience ta
        WHERE ta.circular_id = c.circular_id
        AND (
            /* INDIVIDUAL */
            (
                ta.audience_type = 'INDIVIDUAL'
                AND :user_id = ANY (
                    SELECT value::INT
                    FROM jsonb_array_elements_text(ta.audience_ref_id)
                )
            )

            OR

            /* STATION */
            (
                ta.audience_type = 'STATION'
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(ta.audience_ref_id) sid
                    JOIN users u2
                      ON u2.station_id = sid::INT
                     AND u2.user_id = :user_id
                     AND u2.is_deleted = FALSE
                )
            )

            OR

            /* GROUP */
            (
                ta.audience_type = 'GROUP'
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(ta.audience_ref_id) gid
                    JOIN group_master gm
                      ON gm.group_id = gid::INT
                     AND gm.is_deleted = FALSE
                    WHERE :user_id IN (
                        SELECT value::INT
                        FROM jsonb_array_elements_text(gm.employee_ids)
                    )
                )
            )
        )
    )
    THEN ua.is_acknowledged
        ELSE true
    END AS is_acknowledged
        FROM circular_master c
        LEFT JOIN circular_user_activity ua ON c.circular_id = ua.circular_id and ua.user_id = :user_id
        JOIN users u 
            ON u.user_id = c.created_by 
           AND u.is_deleted = FALSE
        LEFT JOIN category_master cat 
            ON cat.category_id = c.category_id 
           AND cat.is_deleted = FALSE
        LEFT JOIN subcategory_master sub 
            ON sub.subcategory_id = c.subcategory_id 
           AND sub.is_deleted = FALSE
    """

    params = {"user_id": user_id}

    # -------------------------------------------------
    # 3️⃣ If Admin → Get All Circulars
    # -------------------------------------------------
    if role and role.lower() in ["admin", "md"]:
        if pu_status and role and role.lower() == 'md' and pu_status.lower() == 'active':
            base_query += """
                         JOIN circular_target_audience ta 
                         ON ta.circular_id = c.circular_id
                         WHERE c.is_deleted = FALSE AND c.is_archived = FALSE
                         AND (
                                /* ========= INDIVIDUAL ========= */
                                    (
                                        ta.audience_type = 'INDIVIDUAL'
                                        AND :user_id = ANY (
                                            SELECT value::INT
                                            FROM jsonb_array_elements_text(ta.audience_ref_id)
                                        )
                                    )

                                    /* ========= STATION ========= */
                                    OR (
                                        ta.audience_type = 'STATION'
                                        AND EXISTS (
                                            SELECT 1
                                            FROM jsonb_array_elements_text(ta.audience_ref_id) sid
                                            JOIN users u2
                                            ON u2.station_id = sid::INT
                                            AND u2.user_id = :user_id
                                            AND u2.is_deleted = FALSE
                                        )
                                    )

                                            /* ========= GROUP ========= */
                                            OR (
                                                ta.audience_type = 'GROUP'
                                                AND EXISTS (
                                                    SELECT 1
                                                    FROM jsonb_array_elements_text(ta.audience_ref_id) gid
                                                JOIN group_master gm
                                                ON gm.group_id = gid::INT
                                                AND gm.is_deleted = FALSE
                                                WHERE :user_id IN (
                                                    SELECT value::INT
                                                    FROM jsonb_array_elements_text(gm.employee_ids)
                                                )
                                            )
                                        )
                                    )
                                    ORDER BY c.created_date DESC
                                """
            return db.execute(
            text(base_query),
            params
            ).mappings().all()
        else:
            base_query += """
            WHERE c.is_deleted = FALSE AND c.is_archived = FALSE
            ORDER BY c.created_date DESC
        """

            return db.execute(
            text(base_query),
            params
            ).mappings().all()
    
    # -------------------------------------------------
    # 4️⃣ Non-Admin → Apply Audience Filtering
    # -------------------------------------------------
    base_query += """
        JOIN circular_target_audience ta 
            ON ta.circular_id = c.circular_id
        WHERE c.is_deleted = FALSE AND c.is_archived = FALSE
        AND (
            /* ========= INDIVIDUAL ========= */
            (
                ta.audience_type = 'INDIVIDUAL'
                AND :user_id = ANY (
                    SELECT value::INT
                    FROM jsonb_array_elements_text(ta.audience_ref_id)
                )
            )

            /* ========= STATION ========= */
            OR (
                ta.audience_type = 'STATION'
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(ta.audience_ref_id) sid
                    JOIN users u2
                      ON u2.station_id = sid::INT
                     AND u2.user_id = :user_id
                     AND u2.is_deleted = FALSE
                )
            )

            /* ========= GROUP ========= */
            OR (
                ta.audience_type = 'GROUP'
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements_text(ta.audience_ref_id) gid
                    JOIN group_master gm
                      ON gm.group_id = gid::INT
                     AND gm.is_deleted = FALSE
                    WHERE :user_id IN (
                        SELECT value::INT
                        FROM jsonb_array_elements_text(gm.employee_ids)
                    )
                )
            )
        )
        ORDER BY c.created_date DESC
    """
    db.execute(text("DROP TABLE IF EXISTS temp_circulars"))
    db.execute(text("""
        CREATE TEMP TABLE temp_circulars (
            circular_id INT,
            document_no TEXT,
            title TEXT,
            content TEXT,
            category_id INT,
            category_name TEXT,
            subcategory_id INT,
            subcategory_name TEXT,
            version TEXT,
            mandatory_status BOOLEAN,
            status TEXT,
            published_date TIMESTAMP,
            created_by INT,
            updated_date TIMESTAMP,
            publisher_name TEXT,
            tags TEXT,
            is_read BOOLEAN,
            is_acknowledged BOOLEAN
        ) ON COMMIT DROP;
        """))

        # 2️⃣ Insert data
    insert_query = f"""
        INSERT INTO temp_circulars
        {base_query}
        """
    db.execute(text(insert_query),{"user_id": user_id})
    

    dashboard_query = """
            WITH history_access AS (
                SELECT DISTINCT ON (h.circular_id)
                    c.circular_id,
                    c.document_no,
                    c.title,
                    c.content,
                    c.category_id,
                    cat.category_name,
                    c.subcategory_id,
                    sub.subcategory_name,
                    c.change_type AS version,
                    c.mandatory_status,
                    c.status,
                    c.created_date AS published_date,
                    c.created_by,
                    c.updated_date,
                    u.username AS publisher_name,
                    c.tags,
                    ua.is_read,
                    COALESCE(ua.is_acknowledged, TRUE) AS is_acknowledged
                FROM circular_target_audience_history h
                JOIN circular_master_history c ON c.circular_id = h.circular_id and h.version = c.change_type
                LEFT JOIN circular_user_activity ua ON c.circular_id = ua.circular_id 
                left join users u ON u.user_id = c.created_by AND u.is_deleted = FALSE
                LEFT JOIN category_master cat ON cat.category_id = c.category_id AND cat.is_deleted = FALSE
                LEFT JOIN subcategory_master sub ON sub.subcategory_id = c.subcategory_id AND sub.is_deleted = FALSE
                WHERE h.removed_user IS NOT NULL
                    AND EXISTS (
                                SELECT 1
                                FROM jsonb_array_elements_text(h.removed_user) val
                                WHERE val::INT = :user_id
                            )
                
            )

            -- ✅ FINAL RESULT
            SELECT * FROM history_access
            """
    insert_dashboard = f"""
        INSERT INTO temp_circulars
        {dashboard_query}
        """
    
    db.execute(text(insert_dashboard),{"user_id": user_id})

    result = db.execute(text("""
        SELECT * FROM temp_circulars
        ORDER BY circular_id DESC
    """)).mappings().all()

    db.commit()


    return result



# def get_employee_circulars(db: Session, user_id: int):
#     query = text("""
#                     SELECT DISTINCT
#                         c.circular_id,
#                         c.title,
#                         cat.category_name,
#                         sub.subcategory_name,
#                         c.change_type as version,
#                         c.created_date AS published_date,
#                         u.username AS publisher_name
#                     FROM circular_master c
#                     JOIN users u ON u.user_id = c.created_by AND u.is_deleted = FALSE
#                     LEFT JOIN category_master cat ON cat.category_id = c.category_id AND cat.is_deleted = FALSE
#                     LEFT JOIN subcategory_master sub ON sub.subcategory_id = c.subcategory_id AND sub.is_deleted = FALSE
#                     JOIN circular_target_audience ta ON ta.circular_id = c.circular_id
#                     WHERE c.is_deleted = FALSE
#     AND (
#     /* ========= INDIVIDUAL ========= */
#     (
#         ta.audience_type IN ('INDIVIDUAL')
#         AND :user_id = ANY (
#             SELECT value::INT
#             FROM jsonb_array_elements_text(ta.audience_ref_id)
#         )
#     )

#     /* ========= STATION ========= */
#     OR (
#         ta.audience_type = 'STATION'
#         AND EXISTS (
#             SELECT 1
#             FROM jsonb_array_elements_text(ta.audience_ref_id) sid
#             JOIN users u2
#               ON u2.station_id = sid::INT
#              AND u2.user_id = :user_id
#              AND u2.is_deleted = FALSE
#         )
#     )

#     /* ========= GROUP ========= */
#     OR (
#         ta.audience_type = 'GROUP'
#         AND EXISTS (
#             SELECT 1
#             FROM jsonb_array_elements_text(ta.audience_ref_id) gid
#             JOIN group_master gm
#               ON gm.group_id = gid::INT
#              AND gm.is_deleted = FALSE
#             WHERE :user_id IN (
#                 SELECT value::INT
#                 FROM jsonb_array_elements_text(gm.employee_ids)
#             )
#         )
#     )
# )
# ORDER BY c.created_date DESC;
#                 """)
#     return db.execute(query, {"user_id": user_id}).mappings().all()

#employee dashbord count api
def get_circular_dashboard_counts(db: Session, user_id: int):
    query = text("""
        WITH audience_expanded AS (
            SELECT
                cta.circular_id,
                cta.audience_type,
                jsonb_array_elements_text(cta.audience_ref_id)::INT AS ref_id
            FROM circular_target_audience cta
        ),

        user_circulars AS (
            SELECT DISTINCT cm.circular_id,
                cm.mandatory_status,cm.is_archived
            FROM circular_master cm
            JOIN audience_expanded ae
              ON ae.circular_id = cm.circular_id
            WHERE cm.is_deleted = FALSE
              AND (
        -- INDIVIDUAL
        (ae.audience_type = 'INDIVIDUAL'
         AND ae.ref_id = :user_id)

     OR
        -- GROUP (employee_ids JSONB in group_master)
        (ae.audience_type = 'GROUP'
         AND EXISTS (
             SELECT 1
             FROM group_master gm,
                  jsonb_array_elements_text(gm.employee_ids) AS emp_id
             WHERE gm.group_id = ae.ref_id
               AND emp_id::INT = :user_id
         ))

     OR
        -- STATION (station_id from users table)
        (ae.audience_type = 'STATION'
         AND ae.ref_id = (
             SELECT station_id
             FROM users
             WHERE user_id = :user_id
         ))
)
        )

        SELECT
            COUNT(DISTINCT uc.circular_id)
                  FILTER (
                WHERE uc.is_archived = false
            ) AS total_circulars,

            COUNT(DISTINCT uc.circular_id)
            FILTER (
                WHERE cua.is_read = FALSE OR cua.is_read IS NULL
            ) AS unread,

            COUNT(DISTINCT uc.circular_id)
            FILTER (
                WHERE uc.mandatory_status = TRUE
            ) AS mandatory,

            COUNT(DISTINCT uc.circular_id)
            FILTER (
                WHERE cua.is_acknowledged = TRUE
            ) AS acknowledged

        FROM user_circulars uc
        LEFT JOIN circular_user_activity cua
          ON cua.circular_id = uc.circular_id
         AND cua.user_id = :user_id
    """)

    result = db.execute(
        query,
        {"user_id": user_id}
    ).mappings().first()

    return {
        "total_circulars": result["total_circulars"],
        "unread": result["unread"],
        "mandatory": result["mandatory"],
        "acknowledged": result["acknowledged"]
    }

