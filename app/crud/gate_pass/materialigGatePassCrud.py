from datetime import datetime
import json
import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.gate_pass.GatePass import InwardMaterialDetailsRequest, OutwardGatePassByUserRequest

from app.schemas.gate_pass.GatePass import InwardMaterialDetailsRequest, OutwardMaterialDetailsRequest


import uuid

def insert_invert_material_details_crud(
    db: Session,
    req,
    goods_photo: UploadFile
):
    try:
        upload_dir = "files/gate_pass"
        os.makedirs(upload_dir, exist_ok=True)

        # ✅ Use UUID to guarantee unique filenames
        unique_id = uuid.uuid4().hex
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}_{goods_photo.filename}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as f:
            f.write(goods_photo.file.read())

        db_photo_path = f"files/gate_pass/{filename}"

        sql = text("""
            SELECT public.insert_inward_material_details(
                :p_inward_id,
                :p_description,
                :p_ordered_quantity,
                :p_received_quantity,
                :p_unit,
                :p_remarks,
                :p_goods_photo
            ) AS result;
        """)

        params = {
            "p_inward_id": req.inward_id,
            "p_description": req.description,
            "p_ordered_quantity": req.ordered_quantity,
            "p_received_quantity": req.received_quantity,
            "p_unit": req.unit,
            "p_remarks": req.remarks,
            "p_goods_photo": db_photo_path
        }

        result = db.execute(sql, params).scalar_one_or_none()
        db.commit()

        return {"message": result}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}
 
 
def insert_outward_material_details_crud(
    db: Session,
    req: OutwardMaterialDetailsRequest,
    goods_photo: UploadFile
):
    try:
        # Save uploaded file
        upload_dir = "files/gate_pass"
        os.makedirs(upload_dir, exist_ok=True)
 
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{goods_photo.filename}"
        file_path = os.path.join(upload_dir, filename)
 
        with open(file_path, "wb") as f:
            f.write(goods_photo.file.read())
 
        db_photo_path = f"files/gate_pass/{filename}"
 
        # Call PostgreSQL function
        sql = text("""
            SELECT public.insert_outward_material_details(
                :p_outward_id,
                :p_description,
                :p_quantity,
                :p_unit,
                :p_returnable,
                :p_returnable_date,
                :p_remarks,
                :p_goods_photo
            ) AS result;
        """)
 
        params = {
            "p_outward_id": req.outward_id,
            "p_description": req.description,
            "p_quantity": req.quantity,
            "p_unit": req.unit,
            "p_returnable": req.returnable,
            "p_returnable_date": req.returnable_date,
            "p_remarks": req.remarks,
            "p_goods_photo": db_photo_path
        }
 
        raw_result = db.execute(sql, params).scalar()
        db.commit()
 
        # -------------------------------
        # FIX: Handle dict OR JSON string
        # -------------------------------
        if raw_result is None:
            return {"error": "Empty response returned from database."}
 
        # If result is a JSON string → parse it
        if isinstance(raw_result, str):
            result_json = json.loads(raw_result)
        else:
            result_json = raw_result  # already a dict
 
        # Handle outward_id not found
        if result_json.get("status_code") == 400:
            return {"error": "Outward ID does not exist in database."}
 
        # Handle DB errors
        if result_json.get("status_code") == 500:
            return {"error": result_json.get("status_message")}
 
        return {"message": result_json}
 
    except Exception as e:
        db.rollback()
        return {"error": f"Database error: {str(e)}"}



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
        """
        Calls the PostgreSQL function insert_returnable_materials_and_photos.
        JSON casting handled entirely in Python using json.dumps().
        """
        query = text("""
            SELECT public.insert_returnable_materials_and_photos(
                :p_gate_pass_no,
                :p_materials,
                :p_vehicle_photo,
                :p_delivery_personnel_photo,
                :p_delivery_personnel_id_photo,
                :p_goods_photo,
                :p_uploaded_by
            ) AS result;
        """)
 
        try:
            result = db.execute(
                query,
                {
                    "p_gate_pass_no": gate_pass_no,
                    "p_materials": json.dumps(materials),  # Convert list of dicts to JSON string
                    "p_vehicle_photo": vehicle_photo,
                    "p_delivery_personnel_photo": delivery_personnel_photo,
                    "p_delivery_personnel_id_photo": delivery_personnel_id_photo,
                    "p_goods_photo": goods_photo,
                    "p_uploaded_by": uploaded_by
                }
            ).fetchone()
 
            db.commit()
            return result[0] if result else {"status": "error", "message": "No response from function"}
 
        except Exception as e:
            db.rollback()
            raise Exception(f"Database error: {str(e)}")




def create_returnable_material_detail(db: Session, data: dict):
    """
    Calls PostgreSQL fn_create_returnable_material_detail() to insert a record
    """
    try:
        query = text("""
            SELECT * FROM fn_create_returnable_material_detail(
                :returnable_id, :description, :actual_quantity,
                :received_quantity, :unit, 
                :condition, :remarks, :goods_photo, :returned_goods_photo
            );
        """)
        result = db.execute(query, data).mappings().first()
        db.commit()
        return dict(result)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
 
 

def get_returnable_material_details(db: Session, detail_id: int = None):
    """
    Calls PostgreSQL fn_get_returnable_material_detail() to fetch record(s)
    """
    try:
        if detail_id:
            query = text("SELECT * FROM fn_get_returnable_material_detail(:p_id);")
            result = db.execute(query, {"p_id": detail_id}).mappings().all()
        else:
            query = text("SELECT * FROM fn_get_returnable_material_detail(NULL);")
            result = db.execute(query).mappings().all()
 
        return [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 

def update_returnable_material_detail(db: Session, detail_id: int, data: dict):
    """
    Calls PostgreSQL fn_update_returnable_material_detail() to update a record
    """
    try:
        data["id"] = detail_id
        query = text("""
            SELECT * FROM fn_update_returnable_material_detail(
                :id, :returnable_id, :description, :actual_quantity,
                :received_quantity, :unit, :po_type, :po_number,
                :condition, :remarks, :goods_photo, :returned_goods_photo
            );
        """)
        result = db.execute(query, data).mappings().first()
        db.commit()
        return dict(result)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

