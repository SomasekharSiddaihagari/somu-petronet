import datetime
import json
import os
from typing import Any, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text


from app.schemas.gate_pass.GatePass import  APIResponse, OutwardGatePassByUserRequest, ReturnableGatePassData, UpdateReturnableGatePassRequest

# def update_returnable_gate_pass_by_outward_id(
#     db: Session,
#     outward_id: int,
#     payload: UpdateReturnableGatePassRequest
# ) -> APIResponse:
 
#     # Updated SQL call (ONLY 5 parameters now)
#     sql = text("""
#         SELECT * FROM fn_update_returnable_gate_pass_by_outward_id(
#             :p_outward_id,
#             :p_returnable_gate_pass_no,
#             :p_approved_by,
#             :p_reviewer_id,
#             :p_status,
#             :p_updated_by
#         );
#     """)
 
#     # Execute the function synchronously
#     result = db.execute(sql, {
#         "p_outward_id": outward_id,
#         "p_returnable_gate_pass_no": payload.returnable_gate_pass_no,
#         "p_approved_by": payload.approved_by,
#         "p_reviewer_id": payload.reviewer_id,
#         "p_status": payload.status,
#         "p_updated_by": payload.updated_by
#     })
 
#     row = result.fetchone()
 
#     if row is None:
#         return APIResponse(
#             status_code=500,
#             status_message="Unexpected error. No result returned.",
#             data=None
#         )
 
#     updated_id = row[0]
#     status_code = row[1]
#     status_message_text = row[3]
 
#     if status_code == 404:
#         return APIResponse(
#             status_code=status_code,
#             status_message=status_message_text,
#             data=None
#         )
 
#     # Commit changes to persist DB updates
#     db.commit()
 
#     # Fetch full updated row from master table
#     fetch_sql = text("""
#         SELECT * FROM returnable_gate_pass
#         WHERE outward_id = :outward_id;
#     """)
 
#     full_row = db.execute(fetch_sql, {"outward_id": outward_id}).fetchone()
 
#     data = ReturnableGatePassData(
#         returnable_id=full_row.returnable_id,
#         outward_id=full_row.outward_id,
#         returnable_gate_pass_no=full_row.returnable_gate_pass_no,
#         approved_by=full_row.approved_by,
#         reviewer_id=full_row.reviewer_id,
#         date_time=full_row.date_time,
#         status=full_row.status,
#         created_by=full_row.created_by,
#         updated_by=full_row.updated_by,
#         created_at=full_row.created_at,
#         updated_at=full_row.updated_at
#     )
 
#     return APIResponse(
#         status_code=status_code,
#         status_message=status_message_text,
#         data=data
#     )
# def update_returnable_gate_pass_by_outward_id(
#     db: Session,
#     outward_id: int,
#     payload: UpdateReturnableGatePassRequest
# ) -> APIResponse:

#     # Check if record exists
#     fetch_sql = text("""
#         SELECT * FROM returnable_gate_pass
#         WHERE outward_id = :outward_id;
#     """)

#     existing_row = db.execute(fetch_sql, {"outward_id": outward_id}).fetchone()

#     if existing_row is None:
#         return APIResponse(
#             status_code=404,
#             status_message=f"No record found for the provided outward_id {outward_id}.",
#             data=None
#         )

#     # Update returnable_gate_pass table
#     update_rgp_sql = text("""
#         UPDATE returnable_gate_pass
#         SET
#             returnable_gate_pass_no = :p_returnable_gate_pass_no,
#             approved_by             = COALESCE(:p_approved_by, approved_by),
#             reviewer_id             = :p_reviewer_id,
#             status                  = :p_status,
#             updated_by              = :p_updated_by,
#             date_time               = NOW(),
#             updated_at              = NOW()
#         WHERE outward_id = :p_outward_id;
#     """)

#     db.execute(update_rgp_sql, {
#         "p_outward_id":              outward_id,
#         "p_returnable_gate_pass_no": payload.returnable_gate_pass_no,
#         "p_approved_by":             payload.approved_by,
#         "p_reviewer_id":             payload.reviewer_id,
#         "p_status":                  payload.status,
#         "p_updated_by":              payload.updated_by
#     })

#     # Also update outward_gate_pass status (same as SQL function did)
#     update_ogp_sql = text("""
#         UPDATE outward_gate_pass
#         SET
#             status     = :p_status,
#             updated_by = :p_updated_by,
#             updated_at = NOW()
#         WHERE outward_id = :p_outward_id;
#     """)

#     db.execute(update_ogp_sql, {
#         "p_outward_id": outward_id,
#         "p_status":     payload.status,
#         "p_updated_by": payload.updated_by
#     })

#     db.commit()

#     # Fetch the updated row
#     updated_row = db.execute(fetch_sql, {"outward_id": outward_id}).fetchone()

#     data = ReturnableGatePassData(
#         returnable_id=updated_row.returnable_id,
#         outward_id=updated_row.outward_id,
#         returnable_gate_pass_no=updated_row.returnable_gate_pass_no,
#         approved_by=updated_row.approved_by,
#         reviewer_id=updated_row.reviewer_id,
#         date_time=updated_row.date_time,
#         status=updated_row.status,
#         created_by=updated_row.created_by,
#         updated_by=updated_row.updated_by,
#         created_at=updated_row.created_at,
#         updated_at=updated_row.updated_at
#     )

#     return APIResponse(
#         status_code=200,
#         status_message="Record updated in returnable_gate_pass and outward_gate_pass successfully.",
#         data=data
#     )


# def update_returnable_gate_pass_by_outward_id(
#     db: Session,
#     outward_id: int,
#     payload: UpdateReturnableGatePassRequest
#     ) -> APIResponse:

#     # Check if record exists
#     fetch_sql = text("""
#         SELECT * FROM returnable_gate_pass
#         WHERE outward_id = :outward_id;
#     """)

#     existing_row = db.execute(fetch_sql, {"outward_id": outward_id}).fetchone()

#     if existing_row is None:
#         return APIResponse(
#             status_code=404,
#             status_message=f"No record found for the provided outward_id {outward_id}.",
#             data=None
#         )

#     # Update returnable_gate_pass — do NOT touch returnable_gate_pass_no
#     update_rgp_sql = text("""
#         UPDATE returnable_gate_pass
#         SET
#             approved_by  = COALESCE(:p_approved_by, approved_by),
#             reviewer_id  = :p_reviewer_id,
#             status       = :p_status,
#             updated_by   = :p_updated_by,
#             date_time    = NOW(),
#             updated_at   = NOW()
#         WHERE outward_id = :p_outward_id;
#     """)

#     db.execute(update_rgp_sql, {
#         "p_outward_id":  outward_id,
#         "p_approved_by": payload.approved_by,
#         "p_reviewer_id": payload.reviewer_id,
#         "p_status":      payload.status,
#         "p_updated_by":  payload.updated_by
#     })

#     # Update outward_gate_pass status
#     update_ogp_sql = text("""
#         UPDATE outward_gate_pass
#         SET
#             status     = :p_status,
#             updated_by = :p_updated_by,
#             updated_at = NOW()
#         WHERE outward_id = :p_outward_id;
#     """)

#     db.execute(update_ogp_sql, {
#         "p_outward_id": outward_id,
#         "p_status":     payload.status,
#         "p_updated_by": payload.updated_by
#     })

#     db.commit()

#     # Fetch the updated row
#     updated_row = db.execute(fetch_sql, {"outward_id": outward_id}).fetchone()

#     data = ReturnableGatePassData(
#         returnable_id=updated_row.returnable_id,
#         outward_id=updated_row.outward_id,
#         returnable_gate_pass_no=updated_row.returnable_gate_pass_no,
#         approved_by=updated_row.approved_by,
#         reviewer_id=updated_row.reviewer_id,
#         date_time=updated_row.date_time,
#         status=updated_row.status,
#         created_by=updated_row.created_by,
#         updated_by=updated_row.updated_by,
#         created_at=updated_row.created_at,
#         updated_at=updated_row.updated_at
#     )

#     return APIResponse(
#         status_code=200,
#         status_message="Record updated successfully.",
#         data=data
#     )

# ── CRUD ──────────────────────────────────────────────────────────────────────
# def update_returnable_gate_pass_by_outward_id(
#     db: Session,
#     outward_id: int,
#     payload: UpdateReturnableGatePassRequest
# ) -> APIResponse:

#     # Check if record exists by both outward_id AND returnable_id
#     fetch_sql = text("""
#         SELECT * FROM returnable_gate_pass
#         WHERE outward_id    = :outward_id
#         AND   returnable_id = :returnable_id;
#     """)

#     existing_row = db.execute(fetch_sql, {
#         "outward_id":    outward_id,
#         "returnable_id": payload.returnable_id
#     }).fetchone()

#     if existing_row is None:
#         return APIResponse(
#             status_code=404,
#             status_message=f"No record found for outward_id {outward_id} and returnable_id {payload.returnable_id}.",
#             data=None
#         )

#     # Update returnable_gate_pass by both ids
#     update_rgp_sql = text("""
#         UPDATE returnable_gate_pass
#         SET
#             approved_by = COALESCE(:p_approved_by, approved_by),
#             reviewer_id = :p_reviewer_id,
#             status      = :p_status,
#             updated_by  = :p_updated_by,
#             date_time   = :p_date_time,
#             updated_at  = NOW()
#         WHERE outward_id    = :p_outward_id
#         AND   returnable_id = :p_returnable_id;
#     """)

#     db.execute(update_rgp_sql, {
#         "p_outward_id":    outward_id,
#         "p_returnable_id": payload.returnable_id,
#         "p_approved_by":   payload.approved_by,
#         "p_reviewer_id":   payload.reviewer_id,
#         "p_status":        payload.status,
#         "p_date_time":     payload.date_time,
#         "p_updated_by":    payload.updated_by
#     })

#     # Update outward_gate_pass status
#     update_ogp_sql = text("""
#         UPDATE outward_gate_pass
#         SET
            
#             updated_by = :p_updated_by,
#             updated_at = NOW()
#         WHERE outward_id = :p_outward_id;
#     """)

#     db.execute(update_ogp_sql, {
#         "p_outward_id": outward_id,
#         "p_updated_by": payload.updated_by
#     })

#     db.commit()

#     # Fetch the updated row
#     updated_row = db.execute(fetch_sql, {
#         "outward_id":    outward_id,
#         "returnable_id": payload.returnable_id
#     }).fetchone()

#     data = ReturnableGatePassData(
#         returnable_id=          updated_row.returnable_id,
#         outward_id=             updated_row.outward_id,
#         returnable_gate_pass_no=updated_row.returnable_gate_pass_no,
#         approved_by=            updated_row.approved_by,
#         reviewer_id=            updated_row.reviewer_id,
#         date_time=              updated_row.date_time,
#         status=                 updated_row.status,
#         created_by=             updated_row.created_by,
#         updated_by=             updated_row.updated_by,
#         created_at=             updated_row.created_at,
#         updated_at=             updated_row.updated_at
#     )

#     return APIResponse(
#         status_code=200,
#         status_message="Record updated successfully.",
#         data=data
#     )
def update_returnable_gate_pass_by_outward_id(
    db: Session,
    outward_id: int,
    payload: UpdateReturnableGatePassRequest
) -> APIResponse:

    fetch_sql = text("""
        SELECT * FROM returnable_gate_pass
        WHERE outward_id    = :outward_id
        AND   returnable_id = :returnable_id;
    """)

    existing_row = db.execute(fetch_sql, {
        "outward_id":    outward_id,
        "returnable_id": payload.returnable_id
    }).fetchone()

    if existing_row is None:
        return APIResponse(
            status_code=404,
            status_message=f"No record found for outward_id {outward_id} and returnable_id {payload.returnable_id}.",
            data=None
        )

    # Update ONLY the specific returnable_gate_pass row
    update_rgp_sql = text("""
        UPDATE returnable_gate_pass
        SET
            approved_by = COALESCE(:p_approved_by, approved_by),
            reviewer_id = COALESCE(:p_reviewer_id, reviewer_id),  -- ✅ prevent null override
            status      = :p_status,
            updated_by  = :p_updated_by,
            date_time   = COALESCE(:p_date_time, date_time),      -- ✅ same here
            updated_at  = NOW()
        WHERE outward_id    = :p_outward_id
        AND   returnable_id = :p_returnable_id;
    """)

    db.execute(update_rgp_sql, {
        "p_outward_id":    outward_id,
        "p_returnable_id": payload.returnable_id,
        "p_approved_by":   payload.approved_by,
        "p_reviewer_id":   payload.reviewer_id,
        "p_status":        payload.status,
        "p_date_time":     payload.date_time,
        "p_updated_by":    payload.updated_by
    })

    # ✅ outward_gate_pass update — DO NOT touch reviewer_id here.
    # reviewer_id belongs to each returnable row, not the shared outward record.
    update_ogp_sql = text("""
        UPDATE outward_gate_pass
        SET
            updated_by = :p_updated_by,
            updated_at = NOW()
        WHERE outward_id = :p_outward_id;
    """)

    db.execute(update_ogp_sql, {
        "p_outward_id": outward_id,
        "p_updated_by": payload.updated_by
    })

    db.commit()

    updated_row = db.execute(fetch_sql, {
        "outward_id":    outward_id,
        "returnable_id": payload.returnable_id
    }).fetchone()

    data = ReturnableGatePassData(
        returnable_id=           updated_row.returnable_id,
        outward_id=              updated_row.outward_id,
        returnable_gate_pass_no= updated_row.returnable_gate_pass_no,
        approved_by=             updated_row.approved_by,
        reviewer_id=             updated_row.reviewer_id,
        date_time=               updated_row.date_time,
        status=                  updated_row.status,
        created_by=              updated_row.created_by,
        updated_by=              updated_row.updated_by,
        created_at=              updated_row.created_at,
        updated_at=              updated_row.updated_at
    )

    return APIResponse(
        status_code=200,
        status_message="Record updated successfully.",
        data=data
    )



# def insert_returnable_materials_and_photos(
#     db: Session,
#     gate_pass_no: str,
#     materials: list,
#     vehicle_photo: str,
#     delivery_personnel_photo: str,
#     delivery_personnel_id_photo: str,
#     goods_photo: str,
#     uploaded_by: str
# ):
#     """
#     Calls the PostgreSQL function insert_returnable_materials_and_photos.
#     JSON casting handled entirely in Python using json.dumps().
#     """

#     query = text("""
#         SELECT public.insert_returnable_materials_and_photos(
#             :p_gate_pass_no,
#             :p_materials,
#             :p_vehicle_photo,
#             :p_delivery_personnel_photo,
#             :p_delivery_personnel_id_photo,
#             :p_goods_photo,
#             :p_uploaded_by
#         ) AS result;
#     """)

#     try:
#         # Convert Python list of dicts to JSON string for PostgreSQL
#         result = db.execute(
#             query,
#             {
#                 "p_gate_pass_no": gate_pass_no,
#                 "p_materials": json.dumps(materials),  # JSON string
#                 "p_vehicle_photo": vehicle_photo,
#                 "p_delivery_personnel_photo": delivery_personnel_photo,
#                 "p_delivery_personnel_id_photo": delivery_personnel_id_photo,
#                 "p_goods_photo": goods_photo,
#                 "p_uploaded_by": uploaded_by
#             }
#         ).fetchone()

#         db.commit()
#         return result[0] if result else {"status": "error", "message": "No response from function"}

#     except Exception as e:
#         db.rollback()
#         raise Exception(f"Database error: {str(e)}")

def insert_returnable_materials_and_photos(
    db: Session,
    gate_pass_no: str,
    materials: list,
    vehicle_photo: str,
    delivery_personnel_photo: str,
    delivery_personnel_id_photo: str,
    goods_photo: str,
    uploaded_by: str
):
    try:
        # 1️⃣ Get the gate pass
        gate_pass = db.execute(
            text("SELECT * FROM returnable_gate_pass WHERE returnable_gate_pass_no = :no"),
            {"no": gate_pass_no}
        ).fetchone()

        if not gate_pass:
            return {"status": "404 | Not Found", "message": "Returnable Gate Pass not found"}

        returnable_id = gate_pass.returnable_id

        # 2️⃣ ✅ FIX: Check if photo record already exists — upsert manually
        existing_photo = db.execute(
            text("SELECT 1 FROM returnable_gate_pass_photos WHERE returnable_id = :rid"),
            {"rid": returnable_id}
        ).fetchone()

        if existing_photo:
            # Update existing photo record
            db.execute(
                text("""
                    UPDATE returnable_gate_pass_photos
                    SET vehicle_photo               = :vehicle_photo,
                        delivery_personnel_photo    = :delivery_personnel_photo,
                        delivery_personnel_id_photo = :delivery_personnel_id_photo,
                        goods_photo                 = :goods_photo,
                        uploaded_by                 = :uploaded_by,
                        uploaded_at                 = NOW()
                    WHERE returnable_id = :rid
                """),
                {
                    "rid": returnable_id,
                    "vehicle_photo": vehicle_photo,
                    "delivery_personnel_photo": delivery_personnel_photo,
                    "delivery_personnel_id_photo": delivery_personnel_id_photo,
                    "goods_photo": goods_photo,
                    "uploaded_by": uploaded_by,
                }
            )
        else:
            # Insert new photo record
            db.execute(
                text("""
                    INSERT INTO returnable_gate_pass_photos (
                        returnable_id, vehicle_photo, delivery_personnel_photo,
                        delivery_personnel_id_photo, goods_photo, uploaded_by, uploaded_at
                    ) VALUES (
                        :rid, :vehicle_photo, :delivery_personnel_photo,
                        :delivery_personnel_id_photo, :goods_photo, :uploaded_by, NOW()
                    )
                """),
                {
                    "rid": returnable_id,
                    "vehicle_photo": vehicle_photo,
                    "delivery_personnel_photo": delivery_personnel_photo,
                    "delivery_personnel_id_photo": delivery_personnel_id_photo,
                    "goods_photo": goods_photo,
                    "uploaded_by": uploaded_by,
                }
            )

        # 3️⃣ Loop through materials — insert or update
        all_returned = True

        for mat in materials:
            returned_qty = float(mat.get("returned_quantity", 0))

            existing_mat = db.execute(
                text("""
                    SELECT actual_quantity, received_quantity
                    FROM returnable_material_details
                    WHERE returnable_id = :rid AND description = :desc
                """),
                {"rid": returnable_id, "desc": mat.get("description")}
            ).fetchone()

            if not existing_mat:
                # Insert new material
                db.execute(
                    text("""
                        INSERT INTO returnable_material_details (
                            returnable_id, description, actual_quantity, received_quantity,
                            unit, condition, remarks, goods_photo, returned_goods_photo
                        ) VALUES (
                            :rid, :description, :actual_quantity, :received_quantity,
                            :unit, :condition, :remarks, :goods_photo, :goods_photo
                        )
                    """),
                    {
                        "rid": returnable_id,
                        "description": mat.get("description"),
                        "actual_quantity": returned_qty,
                        "received_quantity": returned_qty,
                        "unit": mat.get("unit"),
                        "condition": mat.get("condition"),
                        "remarks": mat.get("remarks"),
                        "goods_photo": mat.get("goods_photo"),
                    }
                )
            else:
                actual_qty = float(existing_mat.actual_quantity)
                received_qty = float(existing_mat.received_quantity)

                new_received = min(received_qty + returned_qty, actual_qty)

                db.execute(
                    text("""
                        UPDATE returnable_material_details
                        SET received_quantity    = :received_quantity,
                            returned_goods_photo = :goods_photo,
                            condition            = :condition,
                            remarks              = :remarks
                        WHERE returnable_id = :rid AND description = :desc
                    """),
                    {
                        "rid": returnable_id,
                        "received_quantity": new_received,
                        "goods_photo": mat.get("goods_photo"),
                        "condition": mat.get("condition"),
                        "remarks": mat.get("remarks"),
                        "desc": mat.get("description"),
                    }
                )

                if new_received < actual_qty:
                    all_returned = False

        db.commit()

        return {
            "status": "0000 | Success",
            "message": "Materials and photos inserted successfully",
            "returnable_gate_pass_no": gate_pass_no,
            "all_returned": all_returned
        }

    except Exception as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")


def update_returnable_materials_and_photos(
    db: Session,
    gate_pass_no: str,
    materials: list,
    vehicle_photo: Optional[str],
    delivery_personnel_photo: Optional[str],
    delivery_personnel_id_photo: Optional[str],
    goods_photo: Optional[str],
    uploaded_by: str
):
    """
    Updates existing returnable gate pass materials and photos.
    Only updates photo columns where a new file was provided (non-null).
    """
    try:
        # ── 1. Validate gate pass exists ──────────────────────────────────
        gate_pass = db.execute(
            text("""
                SELECT returnable_id
                FROM returnable_gate_pass
                WHERE returnable_gate_pass_no = :no
            """),
            {"no": gate_pass_no}
        ).fetchone()

        if not gate_pass:
            return {"status": "404 | Not Found", "message": "Returnable Gate Pass not found"}

        returnable_id = gate_pass[0]

        # ── 2. Update photos — only columns where a new file was sent ─────
        photo_updates = {}
        if vehicle_photo:
            photo_updates["vehicle_photo"] = vehicle_photo
        if delivery_personnel_photo:
            photo_updates["delivery_personnel_photo"] = delivery_personnel_photo
        if delivery_personnel_id_photo:
            photo_updates["delivery_personnel_id_photo"] = delivery_personnel_id_photo
        if goods_photo:
            photo_updates["goods_photo"] = goods_photo

        if photo_updates:
            set_clause = ", ".join([f"{col} = :{col}" for col in photo_updates])
            photo_updates["returnable_id"] = returnable_id
            photo_updates["uploaded_by"] = uploaded_by

            db.execute(
                text(f"""
                    UPDATE returnable_gate_pass_photos
                    SET {set_clause},
                        uploaded_by = :uploaded_by,
                        uploaded_at = NOW()
                    WHERE returnable_id = :returnable_id
                """),
                photo_updates
            )

        # ── 3. Update materials ───────────────────────────────────────────
        all_returned = True

        for mat in materials:
            returned_qty = float(mat.get("returned_quantity", 0))

            existing = db.execute(
                text("""
                    SELECT actual_quantity, received_quantity
                    FROM returnable_material_details
                    WHERE returnable_id = :rid
                      AND description = :desc
                """),
                {"rid": returnable_id, "desc": mat.get("description")}
            ).fetchone()

            if existing:
                actual_qty, received_qty = existing
                new_received = min(received_qty + returned_qty, actual_qty)

                db.execute(
                    text("""
                        UPDATE returnable_material_details
                        SET received_quantity    = :received_qty,
                            condition            = :condition,
                            remarks              = :remarks,
                            returned_goods_photo = :goods_photo
                        WHERE returnable_id = :rid
                          AND description   = :desc
                    """),
                    {
                        "received_qty": new_received,
                        "condition":    mat.get("condition"),
                        "remarks":      mat.get("remarks"),
                        "goods_photo":  mat.get("goods_photo"),
                        "rid":          returnable_id,
                        "desc":         mat.get("description"),
                    }
                )

                if new_received < actual_qty:
                    all_returned = False
            else:
                # Material not found — skip or raise, depending on your business rule
                all_returned = False

        db.commit()

        return {
            "status": "0000 | Success",
            "message": "Materials and photos updated successfully",
            "returnable_gate_pass_no": gate_pass_no,
            "all_returned": all_returned
        }

    except Exception as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")


def get_outward_gate_pass_by_user_crud(db: Session, req: OutwardGatePassByUserRequest):
    """
    Calls the PostgreSQL function:
    public.get_outward_gate_pass_by_station(p_user_id bigint)
    """
    try:
        sql = text("""
            SELECT public.get_outward_gate_pass_by_station(:p_user_id)
        """)
        result = db.execute(sql, {"p_user_id": req.user_id}).scalar_one_or_none()

        if result is None:
            return {
                "status_code": 404,
                "status_message": "No records found for this user/station.",
                "data": []
            }

        return result  # Already a JSON response

    except Exception as e:
        db.rollback()
        return {
            "status_code": 500,
            "status_message": f"Database error: {str(e)}",
            "data": []
        }

def create_returnable_gate_pass_from_outward_crud(db, outward_id: int, created_by: str, approver_name: str):
        """
        Calls stored procedure: create_returnable_gate_pass_from_outward
        and returns the JSON result from PostgreSQL.
        """

        sql = text("""
            SELECT public.create_returnable_gate_pass_from_outward(
                :p_outward_id,
                :p_created_by,
                :p_approver_name
            ) AS result;
        """)

        result = db.execute(sql, {
            "p_outward_id": outward_id,
            "p_created_by": created_by,
            "p_approver_name": approver_name
        }).scalar()

        db.commit()

        # Function returns JSONB → convert to Python dict
        if isinstance(result, str):
            import json
            result = json.loads(result)

        return result
 


# def track_returnable_gate_pass_crud(db: Session, outward_id: int, action: str = None):
#     """
#     Track a returnable gate pass and optionally approve it.
#     Ensures station_id, photos, and returnable-only materials are included in the returned JSON.

#     :param db: SQLAlchemy session
#     :param outward_id: ID of the outward gate pass
#     :param action: Optional action, e.g., 'approve' to change status from pending → returnable
#     :return: JSON response from PostgreSQL function including station_id, photos, and materials
#     """
#     try:
#         # Step 1: Fetch created_by & approver_name from outward_gate_pass
#         fetch_query = text("""
#             SELECT created_by, approver_name
#             FROM outward_gate_pass
#             WHERE outward_id = :oid
#         """)
#         record = db.execute(fetch_query, {"oid": outward_id}).fetchone()

#         if not record:
#             return {"status": "error", "message": "Invalid outward_id"}

#         created_by = record[0]
#         approver_name = record[1]

#         # Step 2: Convert approver_name → user_id
#         approver_user_id = None
#         if approver_name:
#             user_query = text("""
#                 SELECT user_id
#                 FROM users
#                 WHERE TRIM(LOWER(first_name) || ' ' || LOWER(last_name)) = TRIM(LOWER(:name))
#                 LIMIT 1
#             """)
#             user_rec = db.execute(user_query, {"name": approver_name}).fetchone()
#             approver_user_id = user_rec[0] if user_rec else None

#         # Step 3: Call PostgreSQL function with optional action
#         call_query = text("""
#             SELECT public.returnable_gate_pass_tracker(
#                 :p_outward_id,
#                 :p_created_by,
#                 :p_approver_id,
#                 :p_action
#             ) AS result;
#         """)

#         result = db.execute(
#             call_query,
#             {
#                 "p_outward_id": outward_id,
#                 "p_created_by": created_by,
#                 "p_approver_id": approver_user_id,
#                 "p_action": action
#             }
#         ).fetchone()

#         db.commit()

#         # Parse raw JSON
#         raw = result[0]
#         if isinstance(raw, str):
#             data = json.loads(raw)
#         else:
#             data = raw

#         # Step 4: Ensure station_id is added for existing returnable GP
#         if "data" in data:
#             if "station_id" not in data["data"] or data["data"]["station_id"] is None:
#                 approved_by_id = data["data"].get("approver_user_id")
#                 if approved_by_id:
#                     station_query = text("""
#                         SELECT station_id
#                         FROM users
#                         WHERE user_id = :uid
#                     """)
#                     station_rec = db.execute(station_query, {"uid": approved_by_id}).fetchone()
#                     if station_rec:
#                         data["data"]["station_id"] = station_rec[0]
#                         # Step 4.1: Fetch reviewer_id from returnable_gate_pass
#             reviewer_query = text("""
#                 SELECT reviewer_id
#                 FROM returnable_gate_pass
#                 WHERE outward_id = :oid
#                 ORDER BY returnable_id DESC
#                 LIMIT 1
#             """)
#             reviewer_rec = db.execute(reviewer_query, {"oid": outward_id}).fetchone()

#             if reviewer_rec:
#                 data["data"]["reviewer_id"] = reviewer_rec[0]

#             # Step 5: Fetch and inject real photos from outward_gate_pass_photos
#             photos_query = text("""
#                 SELECT
#                     id,
#                     outward_id,
#                     vehicle_photo,
#                     delivery_personnel_photo,
#                     delivery_personnel_id_photo,
#                     goods_photo,
#                     uploaded_by,
#                     uploaded_at
#                 FROM outward_gate_pass_photos
#                 WHERE outward_id = :oid
#             """)
#             photos_rows = db.execute(photos_query, {"oid": outward_id}).fetchall()

#             photos_list = []
#             for row in photos_rows:
#                 photos_list.append({
#                     "id": row[0],
#                     "outward_id": row[1],
#                     "vehicle_photo": row[2],
#                     "delivery_personnel_photo": row[3],
#                     "delivery_personnel_id_photo": row[4],
#                     "goods_photo": row[5],
#                     "uploaded_by": row[6],
#                     "uploaded_at": row[7].isoformat() if row[7] else None
#                 })

#             data["data"]["photos"] = photos_list

#             # Step 6: Fetch materials where returnable = True only
#             materials_query = text("""
#                 SELECT
#                     id,
#                     outward_id,
#                     description,
#                     quantity,
#                     unit,
#                     returnable,
#                     remarks,
#                     goods_photo
#                 FROM outward_material_details
#                 WHERE outward_id = :oid
#                 AND returnable = TRUE
#             """)
#             materials_rows = db.execute(materials_query, {"oid": outward_id}).fetchall()

#             materials_list = []
#             for row in materials_rows:
#                 materials_list.append({
#                     "id": row[0],
#                     "outward_id": row[1],
#                     "description": row[2],
#                     "actual_quantity": row[3],
#                     "unit": row[4],
#                     "returnable": row[5],
#                     "remarks": row[6],
#                     "goods_photo": row[7],
#                     "received_quantity": 0
#                 })

#             data["data"]["materials"] = materials_list

#         return data

#     except Exception as e:
#         db.rollback()
#         raise Exception(f"Database error: {str(e)}")

def track_returnable_gate_pass_crud(db: Session, outward_id: int, action: str = None):
    """
    Track a returnable gate pass and optionally approve it.
    Ensures station_id, photos, and returnable-only materials are included in the returned JSON.

    :param db: SQLAlchemy session
    :param outward_id: ID of the outward gate pass
    :param action: Optional action, e.g., 'approve' to change status from pending → returnable
    :return: JSON response from PostgreSQL function including station_id, photos, and materials
    """
    try:
        # Step 1: Fetch created_by & approver_name from outward_gate_pass
        fetch_query = text("""
            SELECT created_by, approver_name
            FROM outward_gate_pass
            WHERE outward_id = :oid
        """)
        record = db.execute(fetch_query, {"oid": outward_id}).fetchone()

        if not record:
            return {"status": "error", "message": "Invalid outward_id"}

        created_by = record[0]
        approver_name = record[1]

        # Step 2: Convert approver_name → user_id
        approver_user_id = None
        if approver_name:
            user_query = text("""
                SELECT user_id
                FROM users
                WHERE TRIM(LOWER(first_name) || ' ' || LOWER(last_name)) = TRIM(LOWER(:name))
                LIMIT 1
            """)
            user_rec = db.execute(user_query, {"name": approver_name}).fetchone()
            approver_user_id = user_rec[0] if user_rec else None

        # Step 3: Call PostgreSQL function with optional action
        call_query = text("""
            SELECT public.returnable_gate_pass_tracker(
                :p_outward_id,
                :p_created_by,
                :p_approver_id,
                :p_action
            ) AS result;
        """)

        result = db.execute(
            call_query,
            {
                "p_outward_id": outward_id,
                "p_created_by": created_by,
                "p_approver_id": approver_user_id,
                "p_action": action
            }
        ).fetchone()

        db.commit()

        # Parse raw JSON
        raw = result[0]
        if isinstance(raw, str):
            data = json.loads(raw)
        else:
            data = raw

        # Step 4: Ensure station_id is added for existing returnable GP
        if "data" in data:
            if "station_id" not in data["data"] or data["data"]["station_id"] is None:
                approved_by_id = data["data"].get("approver_user_id")
                if approved_by_id:
                    station_query = text("""
                        SELECT station_id
                        FROM users
                        WHERE user_id = :uid
                    """)
                    station_rec = db.execute(station_query, {"uid": approved_by_id}).fetchone()
                    if station_rec:
                        data["data"]["station_id"] = station_rec[0]

            # Step 5: Fetch and inject real photos from outward_gate_pass_photos
            photos_query = text("""
                SELECT
                    id,
                    outward_id,
                    vehicle_photo,
                    delivery_personnel_photo,
                    delivery_personnel_id_photo,
                    goods_photo,
                    uploaded_by,
                    uploaded_at
                FROM outward_gate_pass_photos
                WHERE outward_id = :oid
            """)
            photos_rows = db.execute(photos_query, {"oid": outward_id}).fetchall()

            photos_list = []
            for row in photos_rows:
                photos_list.append({
                    "id": row[0],
                    "outward_id": row[1],
                    "vehicle_photo": row[2],
                    "delivery_personnel_photo": row[3],
                    "delivery_personnel_id_photo": row[4],
                    "goods_photo": row[5],
                    "uploaded_by": row[6],
                    "uploaded_at": row[7].isoformat() if row[7] else None
                })

            data["data"]["photos"] = photos_list

            # Step 6: Fetch materials where returnable = True only
            # JOIN with returnable_material_details to get received_quantity
            # Step 6: Fetch materials where returnable = True only
            # JOIN with returnable_material_details to get received_quantity
            materials_query = text("""
                SELECT
                    omd.id,
                    omd.outward_id,
                    omd.description,
                    omd.quantity,
                    omd.unit,
                    omd.returnable,
                    omd.remarks,
                    omd.goods_photo,
                    COALESCE(rmd.received_quantity, 0) as received_quantity
                FROM outward_material_details omd
                LEFT JOIN returnable_gate_pass rgp 
                    ON rgp.outward_id = omd.outward_id
                LEFT JOIN returnable_material_details rmd 
                    ON rmd.returnable_id = rgp.returnable_id
                    AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
                WHERE omd.outward_id = :oid
                AND omd.returnable = TRUE
            """)
            materials_rows = db.execute(materials_query, {"oid": outward_id}).fetchall()

            materials_list = []
            for row in materials_rows:
                materials_list.append({
                    "id": row[0],
                    "outward_id": row[1],
                    "description": row[2],
                    "actual_quantity": row[3],
                    "unit": row[4],
                    "returnable": row[5],
                    "remarks": row[6],
                    "goods_photo": row[7],
                    "received_quantity": row[8] if row[8] is not None else 0
                })

            data["data"]["materials"] = materials_list
            materials_rows = db.execute(materials_query, {"oid": outward_id}).fetchall()

            materials_list = []
            for row in materials_rows:
                materials_list.append({
                    "id": row[0],
                    "outward_id": row[1],
                    "description": row[2],
                    "actual_quantity": row[3],
                    "unit": row[4],
                    "returnable": row[5],
                    "remarks": row[6],
                    "goods_photo": row[7],
                    "received_quantity": row[8] if row[8] is not None else 0
                })

            data["data"]["materials"] = materials_list

        return data

    except Exception as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")



import json
from sqlalchemy import text
from sqlalchemy.orm import Session
BASE_URL = os.getenv("BackEndPath")


def make_download_url(path: str | None):
    if not path:
        return None

    # Normalize slashes
    normalized = path.replace("\\", "/")

    # Find "files/" index
    idx = normalized.lower().find("files/")
    if idx != -1:
        relative_path = normalized[idx:]
    else:
        # fallback to filename only
        relative_path = os.path.basename(normalized)

    return f"{BASE_URL}/{relative_path}"



from sqlalchemy.orm import Session
from sqlalchemy import text
import json





def track_returnable_gate_pass_crud(db: Session, outward_id: int, action: str = None):
    """
    Production safe tracker

    ✔ Works if returnable exists
    ✔ Works if returnable NOT created
    ✔ Returns full outward data always
    ✔ Includes photos + materials
    ✔ Prevents NOT NULL crash
    ✔ Cumulative pending quantity per material
    ✔ Includes returnable_id + returnable_material_id per material row
    """

    try:

        # --------------------------------------------------
        # STEP 1: Fetch outward base info
        # --------------------------------------------------
        outward_query = text("""
            SELECT *
            FROM outward_gate_pass
            WHERE outward_id = :oid
        """)
        outward_row = db.execute(outward_query, {"oid": outward_id}).mappings().fetchone()

        if not outward_row:
            return {"status": "error", "message": "Invalid outward_id"}

        created_by    = outward_row["created_by"]
        approver_name = outward_row.get("approver_name")

        # --------------------------------------------------
        # STEP 2: Convert approver_name → user_id
        # --------------------------------------------------
        approver_user_id = None
        if approver_name:
            user_query = text("""
                SELECT user_id
                FROM users
                WHERE TRIM(LOWER(first_name) || ' ' || LOWER(last_name)) = TRIM(LOWER(:name))
                LIMIT 1
            """)
            user_rec         = db.execute(user_query, {"name": approver_name}).fetchone()
            approver_user_id = user_rec[0] if user_rec else None

        # --------------------------------------------------
        # STEP 3: Try calling PostgreSQL function
        # --------------------------------------------------
        try:
            call_query = text("""
                SELECT public.returnable_gate_pass_tracker(
                    :p_outward_id,
                    :p_created_by,
                    :p_approver_id,
                    :p_action
                ) AS result;
            """)

            result = db.execute(
                call_query,
                {
                    "p_outward_id":  outward_id,
                    "p_created_by":  created_by,
                    "p_approver_id": approver_user_id,
                    "p_action":      action
                }
            ).fetchone()

            db.commit()

            raw  = result[0]
            data = json.loads(raw) if isinstance(raw, str) else raw

            if "data" not in data:
                data["data"] = dict(outward_row)

        except Exception as func_error:

            db.rollback()

            if "returnable_gate_pass" in str(func_error):
                data = {
                    "status":  "success",
                    "message": "Returnable not created yet — showing outward data",
                    "data":    dict(outward_row)
                }
            else:
                raise func_error

        # --------------------------------------------------
        # STEP 4: Fix station_id if missing
        # --------------------------------------------------
        if not data["data"].get("station_id"):
            approved_by_id = data["data"].get("approver_user_id")
            if approved_by_id:
                station_query = text("""
                    SELECT station_id FROM users WHERE user_id = :uid
                """)
                station_rec = db.execute(station_query, {"uid": approved_by_id}).fetchone()
                if station_rec:
                    data["data"]["station_id"] = station_rec[0]

        # --------------------------------------------------
        # STEP 5: Outward Photos
        # --------------------------------------------------
        photos_query = text("""
            SELECT id, outward_id, vehicle_photo,
                   delivery_personnel_photo,
                   delivery_personnel_id_photo,
                   goods_photo, uploaded_by, uploaded_at
            FROM outward_gate_pass_photos
            WHERE outward_id = :oid
        """)
        photos_rows = db.execute(photos_query, {"oid": outward_id}).fetchall()

        data["data"]["photos"] = [
            {
                "id":                           r[0],
                "outward_id":                   r[1],
                "vehicle_photo":                make_download_url(r[2]),
                "delivery_personnel_photo":     make_download_url(r[3]),
                "delivery_personnel_id_photo":  make_download_url(r[4]),
                "goods_photo":                  make_download_url(r[5]),
                "uploaded_by":                  r[6],
                "uploaded_at":                  r[7].isoformat() if r[7] else None
            }
            for r in photos_rows
        ]

        # --------------------------------------------------
        # STEP 6: Get ALL returnables for this outward_id
        # --------------------------------------------------
        all_returnables_query = text("""
            SELECT
                returnable_id,
                returnable_gate_pass_no,
                outward_id,
                approved_by,
                date_time,
                status,
                created_by,
                station,
                department_contractor_name,
                purpose,
                address,
                material_taken_by,
                vehicle_no,
                driver_phone,
                date_time_ret
            FROM returnable_gate_pass
            WHERE outward_id = :oid
            ORDER BY returnable_id ASC
        """)
        all_returnable_rows = db.execute(all_returnables_query, {"oid": outward_id}).fetchall()

        # For backward compat: keep single returnable_date_time as the latest approved one
        latest_returnable = all_returnable_rows[-1] if all_returnable_rows else None

        # --------------------------------------------------
        # STEP 7: Returnable Photos — fetch for ALL returnables
        # --------------------------------------------------
        returnables_list = []

        for ret_row in all_returnable_rows:
            r_id = ret_row[0]

            returnable_photos_query = text("""
                SELECT
                    rp.id, rp.returnable_id, rp.vehicle_photo,
                    rp.delivery_personnel_photo,
                    rp.delivery_personnel_id_photo,
                    rp.goods_photo, rp.uploaded_by, rp.uploaded_at,
                    u.first_name, u.last_name
                FROM returnable_gate_pass_photos rp
                LEFT JOIN users u
                    ON u.user_id = CAST(rp.uploaded_by AS INTEGER)
                WHERE rp.returnable_id = :rid
            """)
            photo_rows = db.execute(returnable_photos_query, {"rid": r_id}).fetchall()

            photos = [
                {
                    "id":                           p[0],
                    "returnable_id":                p[1],
                    "vehicle_photo":                make_download_url(p[2]),
                    "delivery_personnel_photo":     make_download_url(p[3]),
                    "delivery_personnel_id_photo":  make_download_url(p[4]),
                    "goods_photo":                  make_download_url(p[5]),
                    "uploaded_by":                  p[6],
                    "uploaded_by_name":             f"{p[8]} {p[9]}".strip() if p[8] or p[9] else None,
                    "uploaded_at":                  p[7].isoformat() if p[7] else None
                }
                for p in photo_rows
            ]

            returnables_list.append({
                "returnable_id":            ret_row[0],
                "returnable_gate_pass_no":  ret_row[1],
                "outward_id":               ret_row[2],
                "approved_by":              ret_row[3],
                "date_time":                ret_row[4].isoformat() if ret_row[4] else None,
                "status":                   ret_row[5],
                "created_by":               ret_row[6],
                "station":                  ret_row[7],
                "department_contractor_name": ret_row[8],
                "purpose":                  ret_row[9],
                "address":                  ret_row[10],
                "material_taken_by":        ret_row[11],
                "vehicle_no":               ret_row[12],
                "driver_phone":             ret_row[13],
                "date_time_ret":            ret_row[14].isoformat() if ret_row[14] else None,
                "photos":                   photos
            })

        # Attach to response
        data["data"]["returnables"] = returnables_list

        # Keep legacy fields pointing to latest returnable (backward compat)
        if latest_returnable:
            data["data"]["returnable_date_time"] = (
                latest_returnable[4].isoformat() if latest_returnable[4] else None
            )
            # Flatten latest returnable's photos into old key for backward compat
            data["data"]["returnable_photos"] = returnables_list[-1]["photos"] if returnables_list else []
        else:
            data["data"]["returnable_date_time"] = None
            data["data"]["returnable_photos"]    = []

        # --------------------------------------------------
        # STEP 8: Materials (cumulative pending per material)
        # --------------------------------------------------

        materials_query = text("""
            SELECT
                omd.id                              AS material_id,
                omd.outward_id,
                omd.description,
                omd.quantity                        AS actual_quantity,
                omd.unit,
                omd.returnable,
                omd.returnable_date,
                omd.remarks,
                omd.goods_photo,
                COALESCE(rmd.received_quantity, 0)  AS received_quantity,
                rgp.returnable_id,
                rmd.id                              AS returnable_material_id,
                rgp.status                          AS returnable_status   -- ← added
            FROM outward_material_details omd
            LEFT JOIN returnable_gate_pass rgp
                ON rgp.outward_id = omd.outward_id
            LEFT JOIN returnable_material_details rmd
                ON rmd.returnable_id = rgp.returnable_id
                AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
            WHERE omd.outward_id = :oid
            AND omd.returnable = TRUE
            ORDER BY omd.id, rgp.returnable_id
        """)
        materials_rows = db.execute(materials_query, {"oid": outward_id}).fetchall()

        running_pending = {}
        materials_list  = []

        for r in materials_rows:
            material_id       = r[0]
            actual_qty        = float(r[3] or 0)
            received_qty      = float(r[9] or 0)
            returnable_status = r[12]

            # First time seeing this material → start from actual_quantity
            if material_id not in running_pending:
                running_pending[material_id] = actual_qty

            is_rejected = returnable_status == "Returnable Rejected"

            if is_rejected:
                # ← rejected: do NOT deduct received_qty, pending stays same as before
                pending_qty  = running_pending[material_id]
                received_qty = 0.0   # show 0 so frontend knows nothing was counted
            else:
                # normal: deduct received from running pending
                pending_qty = running_pending[material_id] - received_qty
                running_pending[material_id] = pending_qty  # update only if not rejected

            materials_list.append({
                "id":                       r[0],
                "outward_id":               r[1],
                "description":              r[2],
                "actual_quantity":          actual_qty,
                "unit":                     r[4],
                "returnable":               r[5],
                "returnable_date":          r[6],
                "remarks":                  r[7],
                "goods_photo":              make_download_url(r[8]),
                "received_quantity":        received_qty,
                "pending_quantity":         pending_qty,
                "returnable_id":            r[10],
                "returnable_material_id":   r[11],
                "returnable_status":        returnable_status,   # ← so frontend can show badge
            })

        data["data"]["materials"] = materials_list

        return data

    except Exception as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")





import json
from sqlalchemy import text
from typing import Any


def rg_get_by_station(db: Session, user_id: int) -> Any:
    try:
        result = db.execute(
            text("""
                SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;
            """),
            {"user_id": user_id}
        ).fetchone()

        if not result or not result[0]:
            return {
                "status_code": 500,
                "status_message": "Unexpected error: No data returned",
                "data": [],
                "security": []
            }

        raw = result[0]
        data = json.loads(raw) if isinstance(raw, str) else raw

        if "data" in data and isinstance(data["data"], list):

            for item in data["data"]:
                outward_id = item.get("outward_id")

                # --- Inject reviewer_id ---
                if outward_id:
                    reviewer_query = text("""
                        SELECT reviewer_id
                        FROM returnable_gate_pass
                        WHERE outward_id = :oid
                        ORDER BY returnable_id DESC
                        LIMIT 1
                    """)
                    reviewer_rec = db.execute(reviewer_query, {"oid": outward_id}).fetchone()
                    item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None

                # --- Inject created_by_name ---
                created_by = item.get("created_by")
                if created_by:
                    try:
                        # Numeric string → query by user_id
                        cb_id = int(created_by)
                        user_row = db.execute(
                            text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                            {"uid": cb_id}
                        ).fetchone()
                    except ValueError:
                        # Non-numeric → query by username
                        user_row = db.execute(
                            text("SELECT first_name, last_name FROM users WHERE username = :uname"),
                            {"uname": created_by}
                        ).fetchone()

                    item["created_by_name"] = f"{user_row[0]} {user_row[1]}".strip() if user_row else None
                else:
                    item["created_by_name"] = None

        return data

    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

# def rg_get_by_station(db: Session, user_id: int) -> Any:
#     try:
#         # ── 1. Fetch returnable gate passes ──────────────────────────────────
#         result = db.execute(
#             text("SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;"),
#             {"user_id": user_id}
#         ).fetchone()

#         if not result or not result[0]:
#             return {
#                 "status_code": 500,
#                 "status_message": "Unexpected error: No data returned",
#                 "data": [],
#                 "security": []
#             }

#         raw = result[0]
#         data = json.loads(raw) if isinstance(raw, str) else raw

#         def resolve_user_name(value):
#             if not value:
#                 return None
#             try:
#                 user_row = db.execute(
#                     text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
#                     {"uid": int(value)}
#                 ).fetchone()
#             except ValueError:
#                 user_row = db.execute(
#                     text("SELECT first_name, last_name FROM users WHERE username = :uname"),
#                     {"uname": value}
#                 ).fetchone()
#             return f"{user_row[0]} {user_row[1]}".strip() if user_row else None

#         # ── 2. Enrich existing returnable items ──────────────────────────────
#         if "data" in data and isinstance(data["data"], list):
#             for item in data["data"]:
#                 outward_id = item.get("outward_id")

#                 # Inject reviewer_id
#                 if outward_id:
#                     reviewer_rec = db.execute(
#                         text("""
#                             SELECT reviewer_id
#                             FROM returnable_gate_pass
#                             WHERE outward_id = :oid
#                             ORDER BY returnable_id DESC
#                             LIMIT 1
#                         """),
#                         {"oid": outward_id}
#                     ).fetchone()
#                     item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None

#                 # Inject created_by_name
#                 item["created_by_name"] = resolve_user_name(item.get("created_by"))

#         # ── 3. Fetch outward gate passes for this user ───────────────────────
#         outward_result = db.execute(
#             text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
#             {"p_user_id": user_id}
#         ).scalar_one_or_none()

#         if outward_result:
#             outward_data = json.loads(outward_result) if isinstance(outward_result, str) else outward_result
#             outward_items = outward_data if isinstance(outward_data, list) else outward_data.get("data", [])

#             # ── 4. Filter: status == "Verified" AND has at least one returnable material ──
#             verified_returnable = [
#                 item for item in outward_items
#                 if item.get("status") == "Verified"
#                 and any(m.get("returnable") is True for m in item.get("materials", []))
#             ]

#             # ── 5. Enrich and tag each filtered outward item ─────────────────
#             for item in verified_returnable:
#                 item["formtype"] = "outward"
#                 item["created_by_name"] = resolve_user_name(item.get("created_by"))

#             # ── 6. Append to the returnable data list ────────────────────────
#             data.setdefault("data", []).extend(verified_returnable)

#         return data

#     except Exception as e:
#         raise Exception(f"Database error: {str(e)}")


def rg_get_by_station(db: Session, user_id: int) -> Any:
    try:
        # ── 1. Fetch returnable gate passes ──────────────────────────────────
        result = db.execute(
            text("SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;"),
            {"user_id": user_id}
        ).fetchone()

        if not result or not result[0]:
            return {
                "status_code": 500,
                "status_message": "Unexpected error: No data returned",
                "data": [],
                "security": []
            }

        raw  = result[0]
        data = json.loads(raw) if isinstance(raw, str) else raw

        def resolve_user_name(value):
            if not value:
                return None
            try:
                user_row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                    {"uid": int(value)}
                ).fetchone()
            except ValueError:
                user_row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE username = :uname"),
                    {"uname": value}
                ).fetchone()
            return f"{user_row[0]} {user_row[1]}".strip() if user_row else None

        def get_materials(outward_id):
            """
            Returns enriched materials with:
            - actual_quantity
            - received_quantity (sum across non-rejected returnables only)
            - can_return (received < actual)
            """
            rows = db.execute(
                text("""
                    SELECT
                        omd.id,
                        omd.outward_id,
                        omd.description,
                        omd.quantity                        AS actual_quantity,
                        omd.unit,
                        omd.returnable,
                        omd.remarks,
                        omd.goods_photo,
                        COALESCE(SUM(
                            CASE
                                WHEN rgp.status = 'Returnable Rejected' THEN 0  -- ← skip rejected
                                ELSE rmd.received_quantity
                            END
                        ), 0)                               AS received_quantity
                    FROM outward_material_details omd
                    LEFT JOIN returnable_gate_pass rgp
                        ON rgp.outward_id = omd.outward_id
                    LEFT JOIN returnable_material_details rmd
                        ON rmd.returnable_id = rgp.returnable_id
                        AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
                    WHERE omd.outward_id = :oid
                    AND omd.returnable = TRUE
                    GROUP BY omd.id, omd.outward_id, omd.description,
                             omd.quantity, omd.unit, omd.returnable,
                             omd.remarks, omd.goods_photo
                    ORDER BY omd.id
                """),
                {"oid": outward_id}
            ).fetchall()

            return [
                {
                    "id":                r[0],
                    "outward_id":        r[1],
                    "description":       r[2],
                    "actual_quantity":   float(r[3] or 0),
                    "unit":              r[4],
                    "returnable":        r[5],
                    "remarks":           r[6],
                    "goods_photo":       r[7],
                    "received_quantity": float(r[8] or 0),
                    "can_return":        float(r[8] or 0) < float(r[3] or 0)  # ← pending exists
                }
                for r in rows
            ]

        # ── 2. Enrich existing returnable items ──────────────────────────────
        if "data" in data and isinstance(data["data"], list):
            for item in data["data"]:
                outward_id = item.get("outward_id")

                if outward_id:
                    # Inject reviewer_id
                    reviewer_rec = db.execute(
                        text("""
                            SELECT reviewer_id
                            FROM returnable_gate_pass
                            WHERE outward_id = :oid
                            ORDER BY returnable_id DESC
                            LIMIT 1
                        """),
                        {"oid": outward_id}
                    ).fetchone()
                    item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None

                    # ← Inject enriched materials
                    item["materials"] = get_materials(outward_id)

                # Inject created_by_name
                item["created_by_name"] = resolve_user_name(item.get("created_by"))

        # ── 3. Fetch outward gate passes for this user ───────────────────────
        outward_result = db.execute(
            text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
            {"p_user_id": user_id}
        ).scalar_one_or_none()

        if outward_result:
            outward_data  = json.loads(outward_result) if isinstance(outward_result, str) else outward_result
            outward_items = outward_data if isinstance(outward_data, list) else outward_data.get("data", [])

            # ── 4. Filter: status == "Verified" AND has returnable material ──
            verified_returnable = [
                item for item in outward_items
                if item.get("status") == "Verified"
                and any(m.get("returnable") is True for m in item.get("materials", []))
            ]

            # ── 5. Enrich and tag each filtered outward item ─────────────────
            for item in verified_returnable:
                item["formtype"]        = "outward"
                item["created_by_name"] = resolve_user_name(item.get("created_by"))

                # ← Replace outward materials with enriched version
                outward_id = item.get("outward_id")
                if outward_id:
                    item["materials"] = get_materials(outward_id)

            # ── 6. Append to the returnable data list ────────────────────────
            data.setdefault("data", []).extend(verified_returnable)

        return data

    except Exception as e:
        raise Exception(f"Database error: {str(e)}")


# def get_all_gate_passes_by_user(db: Session, user_id: int) -> Any:
#     try:
#         combined_data = {
#             "status_code": 200,
#             "status_message": "Success",
#             "returnable_gate_pass": [],
#             "inward_gate_pass": [],
#             "outward_gate_pass": []
#         }

#         # ─── Shared helper ─────────────────────────────────────────────────
#         def resolve_user_name(value):
#             if not value:
#                 return None

#             # Try as user_id
#             try:
#                 row = db.execute(
#                     text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
#                     {"uid": int(value)}
#                 ).fetchone()

#                 if row:
#                     return f"{row[0]} {row[1]}"
#             except:
#                 pass

#             # Try as username/email
#             row = db.execute(
#                 text("SELECT first_name, last_name FROM users WHERE username = :uname OR email = :uname"),
#                 {"uname": str(value)}
#             ).fetchone()

#             if row:
#                 return f"{row[0]} {row[1]}"

#             # 🔥 FINAL fallback (IMPORTANT)
#             return str(value)

#         # ─── 1. Returnable Gate Pass ───────────────────────────────────────
#         try:
#             result = db.execute(
#                 text("SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;"),
#                 {"user_id": user_id}
#             ).fetchone()

#             if result and result[0]:
#                 raw = result[0]
#                 data = json.loads(raw) if isinstance(raw, str) else raw

#                 if "data" in data and isinstance(data["data"], list):
#                     for item in data["data"]:
#                         outward_id = item.get("outward_id")

#                         if outward_id:
#                             # Inject reviewer_id
#                             reviewer_rec = db.execute(
#                                 text("""
#                                     SELECT reviewer_id FROM returnable_gate_pass
#                                     WHERE outward_id = :oid
#                                     ORDER BY returnable_id DESC LIMIT 1
#                                 """),
#                                 {"oid": outward_id}
#                             ).fetchone()
#                             item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None

#                             # Inject received_quantity fix for materials
#                             materials_rows = db.execute(
#                                 text("""
#                                     SELECT
#                                         omd.id,
#                                         omd.outward_id,
#                                         omd.description,
#                                         omd.quantity,
#                                         omd.unit,
#                                         omd.returnable,
#                                         omd.remarks,
#                                         omd.goods_photo,
#                                         COALESCE(rmd.received_quantity, 0) AS received_quantity
#                                     FROM outward_material_details omd
#                                     LEFT JOIN returnable_gate_pass rgp
#                                         ON rgp.outward_id = omd.outward_id
#                                     LEFT JOIN returnable_material_details rmd
#                                         ON rmd.returnable_id = rgp.returnable_id
#                                         AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
#                                     WHERE omd.outward_id = :oid
#                                     AND omd.returnable = TRUE
#                                 """),
#                                 {"oid": outward_id}
#                             ).fetchall()

#                             item["materials"] = [
#                                 {
#                                     "id": row[0],
#                                     "outward_id": row[1],
#                                     "description": row[2],
#                                     "actual_quantity": row[3],
#                                     "unit": row[4],
#                                     "returnable": row[5],
#                                     "remarks": row[6],
#                                     "goods_photo": row[7],
#                                     "received_quantity": row[8] if row[8] is not None else 0,
#                                     "can_return": (row[8] if row[8] is not None else 0) < row[3]  # ← add this
#                                 }
#                                 for row in materials_rows
#                             ]

#                         item["created_by_name"] = resolve_user_name(item.get("created_by"))

#                     combined_data["returnable_gate_pass"] = data["data"]

#         except Exception as e:
#             combined_data["returnable_gate_pass_error"] = str(e)

#         # ─── 2. Inward Gate Pass ───────────────────────────────────────────
#         try:
#             inward_result = db.execute(
#                 text("SELECT * FROM public.get_all_inward_gate_passes(:user_id)"),
#                 {"user_id": user_id}
#             ).fetchall()

#             inward_list = []
#             for row in inward_result:
#                 item = dict(row._mapping)
#                 item["created_by_name"] = resolve_user_name(item.get("created_by"))
#                 inward_list.append(item)

#             combined_data["inward_gate_pass"] = inward_list

#         except Exception as e:
#             combined_data["inward_gate_pass_error"] = str(e)

#         # ─── 3. Outward Gate Pass ──────────────────────────────────────────
#         # ─── 3. Outward Gate Pass ──────────────────────────────────────────
#         try:
#             outward_result = db.execute(
#                 text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
#                 {"p_user_id": user_id}
#             ).scalar_one_or_none()

#             if outward_result:
#                 parsed = json.loads(outward_result) if isinstance(outward_result, str) else outward_result
#                 items = parsed.get("data", parsed) if isinstance(parsed, dict) else parsed

#                 if isinstance(items, list):
#                     for item in items:
#                         item["created_by_name"] = resolve_user_name(item.get("created_by"))

#                         # ── Inject received_quantity + can_return into outward materials ──
#                         outward_id = item.get("outward_id")
#                         if outward_id and isinstance(item.get("materials"), list):
#                             received_rows = db.execute(
#                                 text("""
#                                     SELECT
#                                         LOWER(TRIM(rmd.description)),
#                                         COALESCE(SUM(rmd.received_quantity), 0)
#                                     FROM returnable_gate_pass rgp
#                                     JOIN returnable_material_details rmd
#                                         ON rmd.returnable_id = rgp.returnable_id
#                                     WHERE rgp.outward_id = :oid
#                                     GROUP BY LOWER(TRIM(rmd.description))
#                                 """),
#                                 {"oid": outward_id}
#                             ).fetchall()

#                             # Build a lookup: description → total received
#                             received_map = {row[0]: row[1] for row in received_rows}

#                             for material in item["materials"]:
#                                 qty = material.get("quantity", 0)
#                                 received = received_map.get(
#                                     material.get("description", "").lower().strip(), 0
#                                 )
#                                 material["received_quantity"] = received
#                                 material["can_return"] = received < qty

#                 combined_data["outward_gate_pass"] = items

#         except Exception as e:
#             combined_data["outward_gate_pass_error"] = str(e)

#         return combined_data

#     except Exception as e:
#         return {
#             "status_code": 500,
#             "status_message": f"Database error: {str(e)}",
#             "returnable_gate_pass": [],
#             "inward_gate_pass": [],
#             "outward_gate_pass": []
#         }

def get_all_gate_passes_by_user(db: Session, user_id: int) -> Any:
    try:
        combined_data = {
            "status_code": 200,
            "status_message": "Success",
            "returnable_gate_pass": [],
            "inward_gate_pass": [],
            "outward_gate_pass": []
        }

        # ─── Shared helpers ─────────────────────────────────────────────────
        def resolve_user_name(value):
            if not value:
                return None
            try:
                row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                    {"uid": int(value)}
                ).fetchone()
                if row:
                    return f"{row[0]} {row[1]}"
            except:
                pass
            row = db.execute(
                text("SELECT first_name, last_name FROM users WHERE username = :uname OR email = :uname"),
                {"uname": str(value)}
            ).fetchone()
            if row:
                return f"{row[0]} {row[1]}"
            return str(value)

        # ─── KEY FIX: shared materials helper (same logic as rg_get_by_station) ──
        def get_materials(outward_id: int) -> list:
            """
            Returns one row per material, with:
            - received_quantity = SUM across non-rejected RGPs only
            - can_return        = received < actual
            """
            rows = db.execute(
                text("""
                    SELECT
                        omd.id,
                        omd.outward_id,
                        omd.description,
                        omd.quantity                             AS actual_quantity,
                        omd.unit,
                        omd.returnable,
                        omd.remarks,
                        omd.goods_photo,
                        COALESCE(SUM(
                            CASE
                                WHEN rgp.status = 'Returnable Rejected' THEN 0
                                ELSE COALESCE(rmd.received_quantity, 0)
                            END
                        ), 0)                                    AS received_quantity
                    FROM outward_material_details omd
                    LEFT JOIN returnable_gate_pass rgp
                        ON rgp.outward_id = omd.outward_id
                    LEFT JOIN returnable_material_details rmd
                        ON rmd.returnable_id = rgp.returnable_id
                        AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
                    WHERE omd.outward_id = :oid
                      AND omd.returnable = TRUE
                    GROUP BY omd.id, omd.outward_id, omd.description,
                             omd.quantity, omd.unit, omd.returnable,
                             omd.remarks, omd.goods_photo
                    ORDER BY omd.id
                """),
                {"oid": outward_id}
            ).fetchall()

            return [
                {
                    "id":                row[0],
                    "outward_id":        row[1],
                    "description":       row[2],
                    "actual_quantity":   float(row[3] or 0),
                    "unit":              row[4],
                    "returnable":        row[5],
                    "remarks":           row[6],
                    "goods_photo":       row[7],
                    "received_quantity": float(row[8] or 0),
                    "can_return":        float(row[8] or 0) < float(row[3] or 0),
                }
                for row in rows
            ]

        # ─── 1. Returnable Gate Pass ───────────────────────────────────────
        try:
            result = db.execute(
                text("SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;"),
                {"user_id": user_id}
            ).fetchone()

            if result and result[0]:
                raw  = result[0]
                data = json.loads(raw) if isinstance(raw, str) else raw

                if "data" in data and isinstance(data["data"], list):
                    for item in data["data"]:
                        outward_id   = item.get("outward_id")
                        returnable_id = item.get("returnable_id")  # ✅ use the specific row's id

                        if outward_id:
                            # ✅ FIXED - fetch reviewer_id for THIS specific returnable, not the latest one
                            if returnable_id:
                                reviewer_rec = db.execute(
                                    text("""
                                        SELECT reviewer_id FROM returnable_gate_pass
                                        WHERE returnable_id = :rid
                                    """),
                                    {"rid": returnable_id}
                                ).fetchone()
                                item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None
                            else:
                                item["reviewer_id"] = None

                            item["materials"] = get_materials(outward_id)

                        item["created_by_name"] = resolve_user_name(item.get("created_by"))

                    combined_data["returnable_gate_pass"] = data["data"]

        except Exception as e:
            combined_data["returnable_gate_pass_error"] = str(e)

        # ─── 2. Inward Gate Pass ───────────────────────────────────────────
        try:
            inward_result = db.execute(
                text("SELECT * FROM public.get_all_inward_gate_passes(:user_id)"),
                {"user_id": user_id}
            ).fetchall()

            inward_list = []
            for row in inward_result:
                item = dict(row._mapping)
                item["created_by_name"] = resolve_user_name(item.get("created_by"))
                inward_list.append(item)

            combined_data["inward_gate_pass"] = inward_list

        except Exception as e:
            combined_data["inward_gate_pass_error"] = str(e)

        # ─── 3. Outward Gate Pass ──────────────────────────────────────────
        try:
            outward_result = db.execute(
                text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
                {"p_user_id": user_id}
            ).scalar_one_or_none()

            if outward_result:
                parsed = json.loads(outward_result) if isinstance(outward_result, str) else outward_result
                items  = parsed.get("data", parsed) if isinstance(parsed, dict) else parsed

                if isinstance(items, list):
                    for item in items:
                        item["created_by_name"] = resolve_user_name(item.get("created_by"))

                        # ← Use shared helper (fixes sum-including-rejected bug)
                        outward_id = item.get("outward_id")
                        if outward_id and isinstance(item.get("materials"), list):
                            item["materials"] = get_materials(outward_id)

                combined_data["outward_gate_pass"] = items

        except Exception as e:
            combined_data["outward_gate_pass_error"] = str(e)

        return combined_data

    except Exception as e:
        return {
            "status_code": 500,
            "status_message": f"Database error: {str(e)}",
            "returnable_gate_pass": [],
            "inward_gate_pass": [],
            "outward_gate_pass": []
        }



def get_all_gate_passes_crud(db: Session) -> Any:
    try:
        combined_data = {
            "status_code": 200,
            "status_message": "Success",
            "returnable_gate_pass": [],
            "inward_gate_pass": [],
            "outward_gate_pass": []
        }

        # ─── Shared helpers ────────────────────────────────────────────────
        def resolve_user_name(value):
            if not value:
                return None
            try:
                row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                    {"uid": int(value)}
                ).fetchone()
            except (ValueError, TypeError):
                row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE username = :uname"),
                    {"uname": value}
                ).fetchone()
            return f"{row[0]} {row[1]}".strip() if row else None

        def get_approver_name(approver_id):
            if not approver_id:
                return None
            row = db.execute(
                text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                {"uid": approver_id}
            ).fetchone()
            return f"{row[0]} {row[1]}".strip() if row else None

        def get_outward_details(outward_id):
            row = db.execute(
                text("""
                    SELECT
                        gate_pass_no,
                        date_time,
                        station,
                        issuing_authority,
                        department_contractor_name,
                        purpose,
                        address,
                        material_taken_by,
                        vehicle_no,
                        driver_phone,
                        created_by,
                        approver_id
                    FROM outward_gate_pass
                    WHERE outward_id = :oid
                """),
                {"oid": outward_id}
            ).fetchone()

            if not row:
                return {}

            return {
                "gate_pass_no":               row[0],
                "date_time":                  row[1].isoformat() if row[1] else None,
                "station":                    row[2],
                "issuing_authority":          row[3],
                "department_contractor_name": row[4],
                "purpose":                    row[5],
                "address":                    row[6],
                "material_taken_by":          row[7],
                "vehicle_no":                 row[8],
                "driver_phone":               row[9],
                "initiator_name":             resolve_user_name(row[10]),
                "approver_name":              get_approver_name(row[11]),
            }

        def get_returnable_materials(outward_id):
            rows = db.execute(
                text("""
                    SELECT
                        omd.id,
                        omd.outward_id,
                        omd.description,
                        omd.quantity,
                        omd.unit,
                        omd.returnable,
                        omd.remarks,
                        omd.goods_photo,
                        COALESCE(
                            (
                                SELECT SUM(rmd.received_quantity)
                                FROM returnable_gate_pass rgp
                                JOIN returnable_material_details rmd
                                    ON rmd.returnable_id = rgp.returnable_id
                                WHERE rgp.outward_id = omd.outward_id
                                  AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
                            ), 0
                        ) AS received_quantity
                    FROM outward_material_details omd
                    WHERE omd.outward_id = :oid
                      AND omd.returnable = TRUE
                """),
                {"oid": outward_id}
            ).fetchall()

            return [
                {
                    "id":                row[0],
                    "outward_id":        row[1],
                    "description":       row[2],
                    "actual_quantity":   row[3],
                    "unit":              row[4],
                    "returnable":        row[5],
                    "remarks":           row[6],
                    "goods_photo":       row[7],
                    "received_quantity": int(row[8]) if row[8] is not None else 0,
                    "can_return":        (int(row[8]) if row[8] is not None else 0) < row[3],
                }
                for row in rows
            ]

        def get_outward_materials(outward_id):
            rows = db.execute(
                text("""
                    SELECT
                        id,
                        outward_id,
                        description,
                        quantity,
                        unit,
                        returnable,
                        returnable_date,
                        remarks,
                        goods_photo
                    FROM outward_material_details
                    WHERE outward_id = :oid
                """),
                {"oid": outward_id}
            ).fetchall()

            received_rows = db.execute(
                text("""
                    SELECT
                        LOWER(TRIM(rmd.description)),
                        COALESCE(SUM(rmd.received_quantity), 0)
                    FROM returnable_gate_pass rgp
                    JOIN returnable_material_details rmd
                        ON rmd.returnable_id = rgp.returnable_id
                    WHERE rgp.outward_id = :oid
                    GROUP BY LOWER(TRIM(rmd.description))
                """),
                {"oid": outward_id}
            ).fetchall()

            received_map = {r[0]: int(r[1]) for r in received_rows}

            return [
                {
                    "id":                row[0],
                    "outward_id":        row[1],
                    "description":       row[2],
                    "quantity":          row[3],
                    "unit":              row[4],
                    "returnable":        row[5],
                    "returnable_date":   row[6],
                    "remarks":           row[7],
                    "goods_photo":       row[8],
                    "received_quantity": received_map.get(row[2].lower().strip(), 0),
                    "can_return":        received_map.get(row[2].lower().strip(), 0) < row[3],
                }
                for row in rows
            ]

        # ─── 1. Returnable Gate Pass ───────────────────────────────────────
        try:
            rows = db.execute(
                text("""
                    SELECT
                        returnable_id,
                        returnable_gate_pass_no,
                        outward_id,
                        approved_by,
                        date_time,
                        status,
                        created_by,
                        updated_by,
                        created_at,
                        updated_at,
                        reviewer_id
                    FROM returnable_gate_pass
                    ORDER BY returnable_id DESC
                """)
            ).fetchall()

            combined_data["returnable_gate_pass"] = [
                {
                    "formtype":                "returnable",
                    "returnable_id":           row[0],
                    "returnable_gate_pass_no": row[1],
                    "outward_id":              row[2],
                    "approved_by":             row[3],
                    "date_time":               row[4].isoformat() if row[4] else None,
                    "status":                  row[5],
                    "created_by":              row[6],
                    "updated_by":              row[7],
                    "created_at":              row[8].isoformat() if row[8] else None,
                    "updated_at":              row[9].isoformat() if row[9] else None,
                    "reviewer_id":             row[10] if row[10] else 0,
                    "outward_details":         get_outward_details(row[2]),
                    "materials":               get_returnable_materials(row[2]),
                    "created_by_name":         resolve_user_name(row[6]),
                }
                for row in rows
            ]

        except Exception as e:
            combined_data["returnable_gate_pass_error"] = str(e)

        # ─── 2. Inward Gate Pass (FIXED) ───────────────────────────
        try:
            rows = db.execute(
            text("""
                SELECT
                    inward_id,
                    gate_pass_no,
                    date_time,
                    station,
                    received_from,
                    purpose,
                    supplier_address,
                    vehicle_no,
                    driver_phone,
                    status,
                    created_by,
                    updated_by,
                    created_at,
                    updated_at,
                    approver_id,
                    approver_name
                FROM inward_gate_pass
                ORDER BY inward_id DESC
            """)
        ).fetchall()

            inward_list = []

            for row in rows:
                try:
                    material_rows = db.execute(
                        text("""
                            SELECT id, inward_id, description, ordered_quantity, received_quantity, unit, remarks, goods_photo
                            FROM inward_material_details
                            WHERE inward_id = :iid
                        """),
                        {"iid": row[0]}
                    ).fetchall()

                    inward_list.append({
                        "formtype": "inward",
                        "inward_id": row[0],
                        "gate_pass_no": row[1],
                        "date_time": row[2].isoformat() if hasattr(row[2], "isoformat") else row[2],
                        "station": row[3],
                        "department_contractor_name": row[4],
                        "purpose": row[5],
                        "address": row[6],
                        "vehicle_no": row[7],
                        "driver_phone": row[8],
                        "status": row[9],
                        "created_by": row[10],
                        "updated_by": row[11],
                        "created_at": row[12].isoformat() if hasattr(row[12], "isoformat") else row[12],
                        "updated_at": row[13].isoformat() if hasattr(row[13], "isoformat") else row[13],
                        "approver_id": row[14],
                        "issuing_authority": row[15],
                        "approver_name": row[15],
                        "initiator_name": resolve_user_name(row[10]),
                        "created_by_name": resolve_user_name(row[10]),
                        "materials": [
                            {
                                "id": m[0],
                                "inward_id": m[1],
                                "description": m[2],
                                "ordered_quantity": m[3],
                                "received_quantity": m[4],
                                "unit": m[5],
                                "remarks": m[6],
                                "goods_photo": m[7],
                            }
                            for m in material_rows
                        ],
                    })

                except Exception as inner_error:
                    print("❌ Inward error:", inner_error)
                    raise inner_error

            combined_data["inward_gate_pass"] = inward_list

        except Exception as e:
            db.rollback()
            combined_data["inward_gate_pass_error"] = str(e)

        # ─── 3. Outward Gate Pass ──────────────────────────────────────────
        try:
            rows = db.execute(
                text("""
                    SELECT
                        outward_id,
                        gate_pass_no,
                        date_time,
                        station,
                        issuing_authority,
                        department_contractor_name,
                        purpose,
                        address,
                        material_taken_by,
                        vehicle_no,
                        driver_phone,
                        status,
                        created_by,
                        updated_by,
                        created_at,
                        updated_at,
                        approver_id
                    FROM outward_gate_pass
                    ORDER BY outward_id DESC
                """)
            ).fetchall()

            combined_data["outward_gate_pass"] = [
                {
                    "formtype":                   "outward",
                    "approver_id":                row[16],
                    "outward_id":                 row[0],
                    "gate_pass_no":               row[1],
                    "date_time":                  row[2].isoformat() if row[2] else None,
                    "station":                    row[3],
                    "issuing_authority":          row[4],
                    "department_contractor_name": row[5],
                    "purpose":                    row[6],
                    "address":                    row[7],
                    "material_taken_by":          row[8],
                    "vehicle_no":                 row[9],
                    "driver_phone":               row[10],
                    "status":                     row[11],
                    "created_by":                 row[12],
                    "updated_by":                 row[13],
                    "created_at":                 row[14].isoformat() if row[14] else None,
                    "updated_at":                 row[15].isoformat() if row[15] else None,
                    "initiator_name":             resolve_user_name(row[12]),
                    "approver_name":              get_approver_name(row[16]),
                    "materials":                  get_outward_materials(row[0]),
                    "created_by_name":            resolve_user_name(row[12]),
                }
                for row in rows
            ]

        except Exception as e:
            combined_data["outward_gate_pass_error"] = str(e)

        return combined_data

    except Exception as e:
        return {
            "status_code": 500,
            "status_message": f"Database error: {str(e)}",
            "returnable_gate_pass": [],
            "inward_gate_pass": [],
            "outward_gate_pass": []
        }


