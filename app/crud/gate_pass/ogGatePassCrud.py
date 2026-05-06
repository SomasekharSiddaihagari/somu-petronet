import datetime
import json
import os
from alembic.environment import Any
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.gate_pass.GatePass import InwardMaterialDetailsRequest, OutwardGatePassByUserRequest
BASE_URL = os.getenv("BackEndPath")

def create_outward_gate_pass(db, payload):
    try:
        sql = text("""
            SELECT create_outward_gate_pass_with_photos(
                :station,
                :issuing_authority,
                :department_contractor_name,
                :purpose,
                :address,
                :material_taken_by,
                :vehicle_no,
                :driver_phone,
                :initiator_name,
                :approver_name,
                :approver_id,
                :created_by,
                :vehicle_photo,
                :delivery_personnel_photo,
                :delivery_personnel_id_photo,
                :goods_photo,
                :status
            )
        """)

        row = db.execute(sql, {
            "station": payload.station,
            "issuing_authority": payload.issuing_authority,
            "department_contractor_name": payload.department_contractor_name,
            "purpose": payload.purpose,
            "address": payload.address,
            "material_taken_by": payload.material_taken_by,
            "vehicle_no": payload.vehicle_no,
            "driver_phone": payload.driver_phone,
            "initiator_name": payload.initiator_name,
            "approver_name": payload.approver_name,
            "approver_id": payload.approver_id,     # <-- correct position
            "created_by": payload.created_by,
            "vehicle_photo": payload.vehicle_photo,
            "delivery_personnel_photo": payload.delivery_personnel_photo,
            "delivery_personnel_id_photo": payload.delivery_personnel_id_photo,
            "goods_photo": payload.goods_photo,
            "status": payload.status,
        }).fetchone()

        if row is None:
            raise HTTPException(status_code=500, detail="No response from DB function")

        db.commit()
        result_json = row[0]
        return json.loads(result_json) if isinstance(result_json, str) else result_json

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))




def update_outward_gate_pass(db, outward_id: int, payload, file_paths=None):
    """Update Outward Gate Pass text + photos"""

    try:
        sql = text("""
            SELECT update_outward_gate_pass(
                :approver_id,
                :outward_id,
                :purpose,
                :vehicle_no,
                :driver_phone,
                :updated_by,
                :vehicle_photo,
                :delivery_personnel_photo,
                :delivery_personnel_id_photo,
                :goods_photo,
                :status,
                :approved_at   
            )
        """)

        params = {
            "approver_id":  payload.approver_id,
            "outward_id": outward_id,
            "purpose": payload.purpose,
            "vehicle_no": payload.vehicle_no,
            "driver_phone": payload.driver_phone,
            "updated_by": payload.updated_by,
            "vehicle_photo": file_paths.get("vehicle_photo") if file_paths else None,
            "delivery_personnel_photo": file_paths.get("delivery_personnel_photo") if file_paths else None,
            "delivery_personnel_id_photo": file_paths.get("delivery_personnel_id_photo") if file_paths else None,
            "goods_photo": file_paths.get("goods_photo") if file_paths else None,
            "status": payload.status,
            "approved_at": payload.approved_at,
        }

        row = db.execute(sql, params).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="No record found")

        db.commit()

        result = row[0]
        return json.loads(result) if isinstance(result, str) else result

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# def get_outward_gate_pass_by_user_crud(db: Session, user_id: int):

#     try:
#         sql = text("""
#             SELECT public.get_outward_gate_pass_by_station(:p_user_id)
#         """)

#         # Use user_id directly
#         result = db.execute(sql, {"p_user_id": user_id}).scalar_one_or_none()

#         if result is None:
#             return {
#                 "status_code": 404,
#                 "status_message": "No records found for this user/station.",
#                 "data": []
#             }

#         return result  # PostgreSQL function already returns JSON

#     except Exception as e:
#         db.rollback()
#         return {
#             "status_code": 500,
#             "status_message": f"Database error: {str(e)}",
#             "data": []
#         }


# def get_outward_gate_pass_by_user_crud(db: Session, user_id: int) -> Any:
#     try:
#         combined_data = {
#             "status_code": 200,
#             "status_message": "Success",
#             "returnable_gate_pass": [],
#             "inward_gate_pass": [],
#             "outward_gate_pass": []
#         }

#         # ─── Shared helper: resolve user name ──────────────────────────────
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

#         # ─── Shared helper: inject received_quantity + can_return ───────────
#         def inject_material_quantities(outward_id: int) -> list:
#             if not outward_id:
#                 return []

#             raw_rows = db.execute(
#                 text("""
#                     SELECT
#                         id, outward_id, description, quantity,
#                         unit, returnable, returnable_date, remarks, goods_photo
#                     FROM outward_material_details
#                     WHERE outward_id = :oid
#                     ORDER BY id
#                 """),
#                 {"oid": outward_id}
#             ).fetchall()

#             if not raw_rows:
#                 return []

#             materials = [
#                 {
#                     "id":               r[0],
#                     "outward_id":       r[1],
#                     "description":      r[2],
#                     "quantity":         float(r[3] or 0),
#                     "unit":             r[4],
#                     "returnable":       r[5],
#                     "returnable_date":  r[6],
#                     "remarks":          r[7],
#                     "goods_photo":      r[8],
#                 }
#                 for r in raw_rows
#             ]

#             # Sum received qty — skip Returnable Rejected
#             received_rows = db.execute(
#                 text("""
#                     SELECT
#                         LOWER(TRIM(rmd.description))    AS description,
#                         COALESCE(SUM(
#                             CASE
#                                 WHEN rgp.status = 'Returnable Rejected' THEN 0
#                                 ELSE rmd.received_quantity
#                             END
#                         ), 0)                           AS total_received
#                     FROM returnable_gate_pass rgp
#                     JOIN returnable_material_details rmd
#                         ON rmd.returnable_id = rgp.returnable_id
#                     WHERE rgp.outward_id = :oid
#                     GROUP BY LOWER(TRIM(rmd.description))
#                 """),
#                 {"oid": outward_id}
#             ).fetchall()

#             received_map = {row[0]: float(row[1]) for row in received_rows}

#             for material in materials:
#                 qty      = float(material.get("quantity") or 0)
#                 received = received_map.get(
#                     (material.get("description") or "").lower().strip(), 0.0
#                 )
#                 material["received_quantity"] = received
#                 material["can_return"]        = received < qty

#             return materials

#         # ─── Shared helper: parse nested JSON string or list ────────────────
#         def parse_items(raw):
#             if isinstance(raw, str):
#                 try:
#                     return json.loads(raw)
#                 except Exception:
#                     return []
#             elif isinstance(raw, list):
#                 return raw
#             return []

#         # ─── 1. Returnable Gate Pass ───────────────────────────────────────
#         try:
#             result = db.execute(
#                 text("SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;"),
#                 {"user_id": user_id}
#             ).fetchone()

#             if result and result[0]:
#                 raw  = result[0]
#                 data = json.loads(raw) if isinstance(raw, str) else raw

#                 # Parse data list — may be nested JSON string
#                 raw_items = data.get("data", []) if isinstance(data, dict) else data
#                 items     = parse_items(raw_items)
#                 if isinstance(data, dict):
#                     data["data"] = items

#                 for item in items:
#                     outward_id = item.get("outward_id")

#                     if outward_id:
#                         # Inject reviewer_id
#                         reviewer_rec = db.execute(
#                             text("""
#                                 SELECT reviewer_id FROM returnable_gate_pass
#                                 WHERE outward_id = :oid
#                                 ORDER BY returnable_id DESC LIMIT 1
#                             """),
#                             {"oid": outward_id}
#                         ).fetchone()
#                         item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None

#                         # Inject enriched materials
#                         item["materials"] = inject_material_quantities(outward_id)

#                     item["created_by_name"] = resolve_user_name(item.get("created_by"))

#                 combined_data["returnable_gate_pass"] = items

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
#         try:
#             outward_result = db.execute(
#                 text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
#                 {"p_user_id": user_id}
#             ).scalar_one_or_none()

#             if outward_result:
#                 parsed = json.loads(outward_result) if isinstance(outward_result, str) else outward_result

#                 # ← KEY FIX: data["data"] may come back as nested JSON string
#                 raw_items = parsed.get("data", []) if isinstance(parsed, dict) else parsed
#                 items     = parse_items(raw_items)
#                 if isinstance(parsed, dict):
#                     parsed["data"] = items  # replace string with parsed list

#                 for item in items:
#                     item["created_by_name"] = resolve_user_name(item.get("created_by"))

#                     outward_id = item.get("outward_id")
#                     if outward_id:
#                         item["materials"] = inject_material_quantities(outward_id)

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

# def get_outward_gate_pass_by_user_crud(db: Session, user_id: int):
#     try:
#         response = {
#             "status_code": 200,
#             "status_message": "Success",
#             "outward_gate_pass": []
#         }

#         # ─── Helper: resolve user name ──────────────────────────────
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

#         # ─── Helper: inject material data ───────────────────────────
#         def inject_material_quantities(outward_id: int):
#             if not outward_id:
#                 return []

#             raw_rows = db.execute(
#                 text("""
#                     SELECT
#                         id, outward_id, description, quantity,
#                         unit, returnable, returnable_date, remarks, goods_photo
#                     FROM outward_material_details
#                     WHERE outward_id = :oid
#                     ORDER BY id
#                 """),
#                 {"oid": outward_id}
#             ).fetchall()

#             if not raw_rows:
#                 return []

#             materials = [
#                 {
#                     "id": r[0],
#                     "outward_id": r[1],
#                     "description": r[2],
#                     "quantity": float(r[3] or 0),
#                     "unit": r[4],
#                     "returnable": r[5],
#                     "returnable_date": r[6],
#                     "remarks": r[7],
#                     "goods_photo": r[8],
#                 }
#                 for r in raw_rows
#             ]

#             # received qty
#             received_rows = db.execute(
#                 text("""
#                     SELECT
#                         LOWER(TRIM(rmd.description)) AS description,
#                         COALESCE(SUM(
#                             CASE
#                                 WHEN rgp.status = 'Returnable Rejected' THEN 0
#                                 ELSE rmd.received_quantity
#                             END
#                         ), 0) AS total_received
#                     FROM returnable_gate_pass rgp
#                     JOIN returnable_material_details rmd
#                         ON rmd.returnable_id = rgp.returnable_id
#                     WHERE rgp.outward_id = :oid
#                     GROUP BY LOWER(TRIM(rmd.description))
#                 """),
#                 {"oid": outward_id}
#             ).fetchall()

#             received_map = {row[0]: float(row[1]) for row in received_rows}

#             for material in materials:
#                 qty = float(material.get("quantity") or 0)
#                 received = received_map.get(
#                     (material.get("description") or "").lower().strip(), 0.0
#                 )
#                 material["received_quantity"] = received
#                 material["can_return"] = received < qty

#             return materials

#         # ─── Helper: parse JSON safely ───────────────────────────────
#         def parse_items(raw):
#             if isinstance(raw, str):
#                 try:
#                     return json.loads(raw)
#                 except Exception:
#                     return []
#             elif isinstance(raw, list):
#                 return raw
#             return []

#         # ─── MAIN: OUTWARD ONLY ──────────────────────────────────────
#         outward_result = db.execute(
#             text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
#             {"p_user_id": user_id}
#         ).scalar_one_or_none()

#         if outward_result:
#             parsed = json.loads(outward_result) if isinstance(outward_result, str) else outward_result

#             raw_items = parsed.get("data", []) if isinstance(parsed, dict) else parsed
#             items = parse_items(raw_items)

#             for item in items:
#                 item["created_by_name"] = resolve_user_name(item.get("created_by"))

#                 outward_id = item.get("outward_id")
#                 if outward_id:
#                     item["materials"] = inject_material_quantities(outward_id)

#             response["outward_gate_pass"] = items

#         return response

#     except Exception as e:
#         return {
#             "status_code": 500,
#             "status_message": f"Database error: {str(e)}",
#             "outward_gate_pass": []
#         }



def get_outward_gate_pass_by_user_crud(db: Session, user_id: int) -> Any:
    try:
        combined_data = {
            "status_code": 200,
            "status_message": "Success",
            "outward_gate_pass": []
        }

        # ─── Shared helper ─────────────────────────────────────────────────
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

        # ─── 1. Returnable Gate Pass ───────────────────────────────────────
        try:
            result = db.execute(
                text("SELECT public.get_returnable_gate_pass_by_station(:user_id) AS result;"),
                {"user_id": user_id}
            ).fetchone()

            if result and result[0]:
                raw = result[0]
                data = json.loads(raw) if isinstance(raw, str) else raw

                if "data" in data and isinstance(data["data"], list):
                    for item in data["data"]:
                        outward_id = item.get("outward_id")

                        if outward_id:
                            # Inject reviewer_id
                            reviewer_rec = db.execute(
                                text("""
                                    SELECT reviewer_id FROM returnable_gate_pass
                                    WHERE outward_id = :oid
                                    ORDER BY returnable_id DESC LIMIT 1
                                """),
                                {"oid": outward_id}
                            ).fetchone()
                            item["reviewer_id"] = reviewer_rec[0] if reviewer_rec else None

                            # Inject received_quantity fix for materials
                            materials_rows = db.execute(
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
                                        COALESCE(rmd.received_quantity, 0) AS received_quantity
                                    FROM outward_material_details omd
                                    LEFT JOIN returnable_gate_pass rgp
                                        ON rgp.outward_id = omd.outward_id
                                    LEFT JOIN returnable_material_details rmd
                                        ON rmd.returnable_id = rgp.returnable_id
                                        AND LOWER(TRIM(rmd.description)) = LOWER(TRIM(omd.description))
                                    WHERE omd.outward_id = :oid
                                    AND omd.returnable = TRUE
                                """),
                                {"oid": outward_id}
                            ).fetchall()

                            item["materials"] = [
                                {
                                    "id": row[0],
                                    "outward_id": row[1],
                                    "description": row[2],
                                    "actual_quantity": row[3],
                                    "unit": row[4],
                                    "returnable": row[5],
                                    "remarks": row[6],
                                    "goods_photo": row[7],
                                    "received_quantity": row[8] if row[8] is not None else 0,
                                    "can_return": (row[8] if row[8] is not None else 0) < row[3]  # ← add this
                                }
                                for row in materials_rows
                            ]

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
        # ─── 3. Outward Gate Pass ──────────────────────────────────────────
        try:
            outward_result = db.execute(
                text("SELECT public.get_outward_gate_pass_by_station(:p_user_id)"),
                {"p_user_id": user_id}
            ).scalar_one_or_none()

            if outward_result:
                parsed = json.loads(outward_result) if isinstance(outward_result, str) else outward_result
                items = parsed.get("data", parsed) if isinstance(parsed, dict) else parsed

                if isinstance(items, list):
                    for item in items:
                        item["created_by_name"] = resolve_user_name(item.get("created_by"))

                        # ── Inject received_quantity + can_return into outward materials ──
                        outward_id = item.get("outward_id")
                        if outward_id and isinstance(item.get("materials"), list):
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

                            # Build a lookup: description → total received
                            received_map = {row[0]: row[1] for row in received_rows}

                            for material in item["materials"]:
                                qty = material.get("quantity", 0)
                                received = received_map.get(
                                    material.get("description", "").lower().strip(), 0
                                )
                                material["received_quantity"] = received
                                material["can_return"] = received < qty

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



# def get_outward_gate_pass_by_id(db, outward_id: int):
#     try:
#         sql = text("SELECT get_outward_gate_pass_by_id(:outward_id)")
#         row = db.execute(sql, {"outward_id": outward_id}).fetchone()
 
#         if row is None:
#             raise HTTPException(status_code=500, detail="No response from DB function")
 
#         result_json = row[0]
#         result = json.loads(result_json) if isinstance(result_json, str) else result_json
#         return result
 
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def get_outward_gate_pass_by_id(db, outward_id: int):
    try:
        sql = text("SELECT get_outward_gate_pass_by_id(:outward_id)")
        row = db.execute(sql, {"outward_id": outward_id}).fetchone()

        if row is None:
            raise HTTPException(status_code=500, detail="No response from DB function")

        result_json = row[0]
        result = json.loads(result_json) if isinstance(result_json, str) else result_json

   
        outward = result.get("data", {}).get("outward", {})
        updated_by = outward.get("updated_by")
        if updated_by:
            try:
                ub_id = int(updated_by)
                user_row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE user_id = :uid"),
                    {"uid": ub_id}
                ).fetchone()
            except ValueError:
                user_row = db.execute(
                    text("SELECT first_name, last_name FROM users WHERE username = :uname"),
                    {"uname": updated_by}
                ).fetchone()

            outward["updated_by_name"] = f"{user_row[0]} {user_row[1]}".strip() if user_row else None
        else:
            outward["updated_by_name"] = None

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






