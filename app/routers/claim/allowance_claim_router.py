from datetime import date
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text


from typing import List, Optional
from fastapi import Query


from fastapi import UploadFile, File, Form
import os
import shutil
from fastapi import status

# from app.crud.claim.out_of_packet_crud_ import create_admission_child, create_allowance_claim, create_out_of_pocket_entry, get_employee_children_by_user_id, update_admission_child, update_allowance_claim, update_out_of_pocket_entry
from app.crud.claim.claim_notifications_crud import handle_claim_notification
from app.crud.claim.out_of_packet_crud_ import create_admission_child, create_allowance_claim, get_employee_children_by_user_id, insert_allowance_claim_history, update_admission_child, update_allowance_claim
from app.database import get_db
from app.models.claim.allowance_claim import AllowanceClaim
from app.schemas.claim.allowance_claim_schema import AllowanceAdmissionChildCreate, AllowanceAdmissionChildUpdate, AllowanceClaimCreate,AllowanceClaimUpdate, EmployeeChildDropdown




UPLOAD_BASE = "files"

def save_file(upload: UploadFile, folder: str) -> str:
    os.makedirs(f"{UPLOAD_BASE}/{folder}", exist_ok=True)
    file_path = f"{UPLOAD_BASE}/{folder}/{upload.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    return file_path





router = APIRouter(
    prefix="/api/allowance",
    tags=["allowance Claim Entry"]
)


from datetime import datetime, date

def str_to_date(value: str | None):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()

def str_to_bool(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return value.lower() == "true"


@router.post("/claim", status_code=status.HTTP_201_CREATED)
async def create_claim(
    # -------- Required --------
    ra_claim_id: int = Form(...),

    # -------- Employee Info --------
    employee_name: str | None = Form(None),
    employee_id: str | None = Form(None),
    department: str | None = Form(None),
    designation: str | None = Form(None),
    station: str | None = Form(None),
    grade: str | None = Form(None),
    from_location: str | None = Form(None),
    to_location: str | None = Form(None),
    effective_transfer_date: str | None = Form(None),
    claim_date: str | None = Form(None),

    # -------- Travel --------
    travel_from: str | None = Form(None),
    travel_to: str | None = Form(None),
    travel_mode: str | None = Form(None),
    travel_date: str | None = Form(None),
    number_of_passengers: int | None = Form(None),
    travel_amount: float | None = Form(None),
    travel_remarks: str | None = Form(None),
    include_travel: bool | None = Form(None),
    travel_documents: UploadFile | None = File(None),

    # -------- Displacement --------
    displacement_city: str | None = Form(None),
    no_of_days_claimed: int | None = Form(None),
    displacement_rate: float | None = Form(None),
    displacement_amount: float | None = Form(None),
    maximum_eligible_days: int | None = Form(None),
    displacement_remarks: str | None = Form(None),
    include_displacement: bool | None = Form(None),
    displacement_documents: UploadFile | None = File(None),

    # -------- Settling --------
    basic_pay_monthly: float | None = Form(None),
    dearness_allowance_monthly: float | None = Form(None),
    eligible_settling_amount: float | None = Form(None),
    settling_remarks: str | None = Form(None),
    include_settling: bool | None = Form(None),
    settling_documents: UploadFile | None = File(None),

    # -------- Goods Transport --------
    transport_mode: str | None = Form(None),
    transport_distance_km: float | None = Form(None),
    freight_amount: float | None = Form(None),
    goods_transport_remarks: str | None = Form(None),
    amount_claimed_household_transport: float | None = Form(None),
    include_goods_transport: bool | None = Form(None),
    goods_transport_documents: UploadFile | None = File(None),

    # -------- Packaging --------
    amount_claimed_packaging: float | None = Form(None),
    packaging_vendor: str | None = Form(None),
    packaging_bill_no: str | None = Form(None),
    packaging_remarks: str | None = Form(None),
    maximum_eligible_amount_packaging: float | None = Form(None),
    include_packaging: bool | None = Form(None),
    packaging_documents: UploadFile | None = File(None),

    # -------- Insurance --------
    insurance_company: str | None = Form(None),
    policy_no: str | None = Form(None),
    insurance_amount: float | None = Form(None),
    insurance_start_date: str | None = Form(None),
    insurance_end_date: str | None = Form(None),
    insurance_remarks: str | None = Form(None),
    include_insurance: bool | None = Form(None),
    insurance_documents: UploadFile | None = File(None),

    # -------- Vehicle Transport --------
    vehicle_type: str | None = Form(None),
    vehicle_registration_no: str | None = Form(None),
    vehicle_transport_mode: str | None = Form(None),
    vehicle_transport_amount: float | None = Form(None),
    vehicle_transport_distance_km: float | None = Form(None),
    vehicle_transport_remarks: str | None = Form(None),
    include_vehicle_transport: bool | None = Form(None),
    vehicle_transport_documents: UploadFile | None = File(None),


    # -------- Totals --------
    total_travel: float | None = Form(None),
    total_displacement: float | None = Form(None),
    total_settling: float | None = Form(None),
    total_goods_transport: float | None = Form(None),
    total_packaging: float | None = Form(None),
    total_insurance: float | None = Form(None),
    total_vehicle_transport: float | None = Form(None),
    total_admission: float | None = Form(None),
    grand_total: float | None = Form(None),
    settling_no_of_days: int | None = Form(None),
    t_house_hold_rate: float | None = Form(None),
    vehicle_rate: float | None = Form(None),
    remarks: str | None = Form(None),
    status: str | None = Form(None),

    # -------- Audit --------
    created_by: int | None = Form(None),
    updated_by: int | None = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks(), 
    db: Session = Depends(get_db)
):
    
    payload = {
    "ra_claim_id": ra_claim_id,
    "employee_name": employee_name,
    "employee_id": employee_id,
    "department": department,
    "designation": designation,
    "station": station,
    "grade": grade,
    "from_location": from_location,
    "to_location": to_location,
    "effective_transfer_date": effective_transfer_date,
    "claim_date": claim_date,
    "travel_from": travel_from,
    "travel_to": travel_to,
    "travel_mode": travel_mode,
    "travel_date": travel_date,
    "number_of_passengers": number_of_passengers,
    "travel_amount": travel_amount,
    "travel_remarks": travel_remarks,
    "include_travel": include_travel,
    "displacement_city": displacement_city,
    "no_of_days_claimed": no_of_days_claimed,
    "displacement_rate": displacement_rate,
    "displacement_amount": displacement_amount,
    "maximum_eligible_days": maximum_eligible_days,
    "displacement_remarks": displacement_remarks,
    "include_displacement": include_displacement,
    "basic_pay_monthly": basic_pay_monthly,
    "dearness_allowance_monthly": dearness_allowance_monthly,
    "eligible_settling_amount": eligible_settling_amount,
    "settling_remarks": settling_remarks,
    "include_settling": include_settling,
    "transport_mode": transport_mode,
    "transport_distance_km": transport_distance_km,
    "freight_amount": freight_amount,
    "goods_transport_remarks": goods_transport_remarks,
    "amount_claimed_household_transport": amount_claimed_household_transport,
    "include_goods_transport": include_goods_transport,
    "amount_claimed_packaging": amount_claimed_packaging,
    "packaging_vendor": packaging_vendor,
    "packaging_bill_no": packaging_bill_no,
    "packaging_remarks": packaging_remarks,
    "include_packaging": include_packaging,
    "maximum_eligible_amount_packaging": maximum_eligible_amount_packaging,
    "insurance_company": insurance_company,
    "policy_no": policy_no,
    "insurance_amount": insurance_amount,
    "insurance_start_date": insurance_start_date,
    "insurance_end_date": insurance_end_date,
    "insurance_remarks": insurance_remarks,
    "include_insurance": include_insurance,
    "vehicle_type": vehicle_type,
    "vehicle_registration_no": vehicle_registration_no,
    "vehicle_transport_mode": vehicle_transport_mode,
    "vehicle_transport_amount": vehicle_transport_amount,
    "vehicle_transport_distance_km": vehicle_transport_distance_km,
    "vehicle_transport_remarks": vehicle_transport_remarks,
    "include_vehicle_transport": include_vehicle_transport,
    "total_travel": total_travel,
    "total_displacement": total_displacement,
    "total_settling": total_settling,
    "total_goods_transport": total_goods_transport,
    "total_packaging": total_packaging,
    "total_insurance": total_insurance,
    "total_vehicle_transport": total_vehicle_transport,
    "total_admission": total_admission,
    "grand_total": grand_total,

    # 🔴 IMPORTANT
    "settling_no_of_days": settling_no_of_days,
    "t_house_hold_rate": t_house_hold_rate,
    "vehicle_rate": vehicle_rate,

    "remarks": remarks,
    "status": status,
    "created_by": created_by,
    "updated_by": updated_by,
}

    # -------- File handling --------
    file_fields = {
        "travel_documents": ("travel", travel_documents),
        "displacement_documents": ("displacement", displacement_documents),
        "settling_documents": ("settling", settling_documents),
        "goods_transport_documents": ("goods", goods_transport_documents),
        "packaging_documents": ("packaging", packaging_documents),
        "insurance_documents": ("insurance", insurance_documents),
        "vehicle_transport_documents": ("vehicle", vehicle_transport_documents),
    }

    for field, (folder, file) in file_fields.items():
        if file:
            payload[field] = save_file(file, folder)

    data = AllowanceClaimCreate(**payload)
    claim_id = create_allowance_claim(db, data)
# =====================================================
    # 🔔 NOTIFICATION (CREATE)
    # =====================================================
    if status == "Pending Supervisor Approval":

        class DummySheet:
            def __init__(self):
                self.status = status
                self.user_id = created_by
                self.requisition_number = f"AL-{claim_id}"

                # Employee
                self.employee_name = employee_name
                self.employee_id = employee_id
                self.designation = designation
                self.station = station
                self.claim_date = claim_date

                self.from_location = from_location
                self.to_location = to_location
                self.effective_transfer_date = effective_transfer_date

                # ===== FLAGS =====
                self.include_travel = include_travel
                self.include_displacement = include_displacement
                self.include_settling = include_settling
                self.include_goods_transport = include_goods_transport
                self.include_packaging = include_packaging
                self.include_insurance = include_insurance
                self.include_vehicle_transport = include_vehicle_transport

                # ===== TRAVEL =====
                self.travel_from = travel_from
                self.travel_to = travel_to
                self.travel_mode = travel_mode
                self.travel_date = travel_date
                self.number_of_passengers = number_of_passengers
                self.travel_amount = travel_amount
                self.travel_remarks = travel_remarks

                # ===== DISPLACEMENT =====
                self.displacement_city = displacement_city
                self.no_of_days_claimed = no_of_days_claimed
                self.displacement_rate = displacement_rate
                self.displacement_amount = displacement_amount
                self.displacement_remarks = displacement_remarks

                # ===== SETTLING =====
                self.basic_pay_monthly = basic_pay_monthly
                self.dearness_allowance_monthly = dearness_allowance_monthly
                self.eligible_settling_amount = eligible_settling_amount
                self.settling_remarks = settling_remarks

                # ===== GOODS =====
                self.transport_mode = transport_mode
                self.transport_distance_km = transport_distance_km
                self.freight_amount = freight_amount
                self.amount_claimed_household_transport = amount_claimed_household_transport
                self.goods_transport_remarks = goods_transport_remarks

                # ===== PACKAGING =====
                self.packaging_vendor = packaging_vendor
                self.packaging_bill_no = packaging_bill_no
                self.amount_claimed_packaging = amount_claimed_packaging
                self.packaging_remarks = packaging_remarks

                # ===== INSURANCE =====
                self.insurance_company = insurance_company
                self.policy_no = policy_no
                self.insurance_amount = insurance_amount
                self.insurance_start_date = insurance_start_date
                self.insurance_end_date = insurance_end_date
                self.insurance_remarks = insurance_remarks

                # ===== VEHICLE =====
                self.vehicle_type = vehicle_type
                self.vehicle_registration_no = vehicle_registration_no
                self.vehicle_transport_mode = vehicle_transport_mode
                self.vehicle_transport_distance_km = vehicle_transport_distance_km
                self.vehicle_transport_amount = vehicle_transport_amount
                self.vehicle_transport_remarks = vehicle_transport_remarks

                # ===== TOTALS =====
                self.total_travel = total_travel
                self.total_displacement = total_displacement
                self.total_settling = total_settling
                self.total_goods_transport = total_goods_transport
                self.total_packaging = total_packaging
                self.total_insurance = total_insurance
                self.total_vehicle_transport = total_vehicle_transport
                self.grand_total = grand_total

                self.settling_no_of_days=settling_no_of_days
                self.t_house_hold_rate= t_house_hold_rate
                self.vehicle_rate=vehicle_rate

        sheet = DummySheet()

        await handle_claim_notification(
            db=db,
            module_key="allowance",
            sheet=sheet,
            background_tasks=background_tasks
        )
    return {
        "message": "Allowance claim created successfully",
        "allowance_claim_id": claim_id
    }


from datetime import datetime, date
from fastapi import Form, Depends, HTTPException
from sqlalchemy.orm import Session

def to_date(val):
    if not val:
        return None
    if isinstance(val, date):
        return val
    return datetime.strptime(val, "%Y-%m-%d").date()

@router.put("/claim/{claim_id}")
async def update_full_claim(
    claim_id: int,

    employee_name: str | None = Form(None),
    employee_id: str | None = Form(None),
    department: str | None = Form(None),
    designation: str | None = Form(None),
    station: str | None = Form(None),
    grade: str | None = Form(None),
    from_location: str | None = Form(None),
    to_location: str | None = Form(None),
    effective_transfer_date: str | None = Form(None),
    claim_date: str | None = Form(None),

    travel_from: str | None = Form(None),
    travel_to: str | None = Form(None),
    travel_mode: str | None = Form(None),
    travel_date: str | None = Form(None),
    number_of_passengers: int | None = Form(None),
    travel_amount: float | None = Form(None),
    travel_remarks: str | None = Form(None),
    include_travel: bool | None = Form(None),
    travel_documents: UploadFile | None = File(None),

    displacement_city: str | None = Form(None),
    no_of_days_claimed: int | None = Form(None),
    displacement_rate: float | None = Form(None),
    displacement_amount: float | None = Form(None),
    displacement_remarks: str | None = Form(None),
    include_displacement: bool | None = Form(None),
    displacement_documents: UploadFile | None = File(None),

    basic_pay_monthly: float | None = Form(None),
    dearness_allowance_monthly: float | None = Form(None),
    eligible_settling_amount: float | None = Form(None),
    settling_remarks: str | None = Form(None),
    include_settling: bool | None = Form(None),
    settling_documents: UploadFile | None = File(None),

    total_travel: float | None = Form(None),
    total_displacement: float | None = Form(None),
    total_settling: float | None = Form(None),
    grand_total: float | None = Form(None),

    supervisor_comment: str | None = Form(None),
    hr_comment: str | None = Form(None),
    finance_comment: str | None = Form(None),
    updated_by_supervisor: str | None = Form(None),
    updated_by_supervisor_name: str | None = Form(None),
    updated_by_hr: str | None = Form(None),
    updated_by_hr_name: str | None = Form(None),
    updated_by_finance: str | None = Form(None),
    updated_by_finance_name: str | None = Form(None),

    status: str | None = Form(None),
    updated_by: int | None = Form(None),

    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    claim = db.query(AllowanceClaim).filter(
        AllowanceClaim.allowance_claim_id == claim_id
    ).first()

    if not claim:
        raise HTTPException(404, "Claim not found")

    payload = locals().copy()
    payload.pop("db")
    payload.pop("background_tasks")
    payload.pop("claim_id")

    # ---------- file upload ----------
    file_fields = {
        "travel_documents": ("travel", travel_documents),
        "displacement_documents": ("displacement", displacement_documents),
        "settling_documents": ("settling", settling_documents),
    }

    for field, (folder, file) in file_fields.items():
        if file:
            payload[field] = save_file(file, folder)

    # ---------- update ----------
    for key, value in payload.items():
        if value is not None:
            if "updated_by_" in key and "name" not in key:
                setattr(claim, key, to_date(value))
            else:
                setattr(claim, key, value)

    db.commit()
    db.refresh(claim)

    # ---------- history ----------
    insert_allowance_claim_history(db, claim_id)

    # ---------- notification ----------
    if claim.status:
        class DummySheet:
            def __init__(self, c):
                self.status = c.status
                self.user_id = c.created_by
                self.requisition_number = f"AL-{c.allowance_claim_id}"
                self.employee_name = c.employee_name
                self.employee_id = c.employee_id
                self.designation = c.designation
                self.station = c.station
                self.claim_date = c.claim_date
                self.supervisor_comment = c.supervisor_comment
                self.hr_comment = c.hr_comment
                self.finance_comment = c.finance_comment

        sheet = DummySheet(claim)

        await handle_claim_notification(
            db=db,
            module_key="allowance",
            sheet=sheet,
            background_tasks=background_tasks
        )

    return {
        "message": "Claim updated successfully",
        "allowance_claim_id": claim_id
    }























from fastapi import Form, File, UploadFile
from typing import Optional, List
import os, uuid

UPLOAD_DIR = "files/admission_child_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/admission-child")
async def create_child(
    allowance_claim_id: int = Form(...),

    child_name: Optional[str] = Form(None),
    relationship: Optional[str] = Form(None),
    class_studying: Optional[str] = Form(None),
    school_name: Optional[str] = Form(None),
    amount_claimed: Optional[float] = Form(None),
    remarks: Optional[str] = Form(None),
    city_class: Optional[str]= Form(None),
    city_name: Optional[str]= Form(None),
    user_id: Optional[int] = Form(None),
    station_id: Optional[int] = Form(None),

    documents: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    saved_files = []

    if documents:
        for doc in documents:
            ext = os.path.splitext(doc.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"

            # ✅ FULL RELATIVE PATH
            relative_path = os.path.join(UPLOAD_DIR, filename)

            with open(relative_path, "wb") as f:
                f.write(await doc.read())

            saved_files.append(relative_path)

    # ✅ store full paths in DB
    document_names = ",".join(saved_files) if saved_files else None

    payload = AllowanceAdmissionChildCreate(
        allowance_claim_id=allowance_claim_id,
        child_name=child_name,
        relationship=relationship,
        class_studying=class_studying,
        school_name=school_name,
        amount_claimed=amount_claimed,
        remarks=remarks,
        city_class=city_class,
        city_name=city_name,
        
        document_names=document_names,
        user_id=user_id,
        station_id=station_id
    )

    child_id = create_admission_child(db, payload)

    result = db.execute(
        text("""
            SELECT *
            FROM allowance_admission_child
            WHERE allowance_admission_child_id = :id
        """),
        {"id": child_id}
    ).mappings().first()

    return {
        "message": "Admission child created successfully",
        "data": result,
        "documents": saved_files
    }



@router.put("/admission-child/{child_id}")
async def update_child(
    child_id: int,

    child_name: Optional[str] = Form(None),
    relationship: Optional[str] = Form(None),
    class_studying: Optional[str] = Form(None),
    city_name: Optional[str]= Form(None),
    city_class: Optional[str]= Form(None),
    school_name: Optional[str] = Form(None),
    amount_claimed: Optional[float] = Form(None),
    remarks: Optional[str] = Form(None),
    updated_by: Optional[int] = Form(None),
    user_id: Optional[int] = Form(None),
    station_id: Optional[int] = Form(None),
    documents: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    saved_files = []

    if documents:
        for doc in documents:
            ext = os.path.splitext(doc.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"

            # ✅ FULL RELATIVE PATH
            relative_path = os.path.join(UPLOAD_DIR, filename)

            with open(relative_path, "wb") as f:
                f.write(await doc.read())

            saved_files.append(relative_path)

    document_names = ",".join(saved_files) if saved_files else None

    payload = AllowanceAdmissionChildUpdate(
        child_name=child_name,
        relationship=relationship,
        class_studying=class_studying,
        school_name=school_name,
        amount_claimed=amount_claimed,
        remarks=remarks,
        city_class=city_class,
        city_name=city_name,
        document_names=document_names,
        updated_by=updated_by,
        user_id=user_id,
        station_id=station_id
    )

    updated = update_admission_child(db, child_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Admission child not found")

    result = db.execute(
        text("""
            SELECT *
            FROM allowance_admission_child
            WHERE allowance_admission_child_id = :id
        """),
        {"id": child_id}
    ).mappings().first()

    return {
        "message": "Admission child updated successfully",
        "data": result,
        "documents": saved_files
    }




# ---------------------------------------
# ALLOWANCE MAPPING
# ---------------------------------------

ALLOWANCE = {
    "E1": {"bangalore": 1400, "others": 1250},
    "E2": {"bangalore": 1400, "others": 1250},
    "E3": {"bangalore": 1400, "others": 1250},
    "E4": {"bangalore": 1400, "others": 1250},
    "E5": {"bangalore": 1500, "others": 1350},
    "E6": {"bangalore": 1700, "others": 1500},
    "E7": {"bangalore": 1900, "others": 1750},
}

# ---------------------------------------
# REQUEST MODEL
# ---------------------------------------

class DailyAllowanceRequest(BaseModel):
    grade: str
    city: str   # bangalore / others


# ---------------------------------------
# API
# ---------------------------------------

@router.post("/daily-allowance-city")
def get_daily_allowance(payload: DailyAllowanceRequest):

    grade = payload.grade.upper()
    city = payload.city.lower()

    # Validate grade
    if grade not in ALLOWANCE:
        raise HTTPException(status_code=400, detail="Invalid grade")

    # Validate city
    if city not in ["bangalore", "others"]:
        raise HTTPException(
            status_code=400,
            detail="City must be either 'Bangalore' or 'Others'"
        )

    amount = ALLOWANCE[grade][city]

    return {
        "grade": grade,
        "selected_city": city.capitalize(),
        "daily_allowance": amount
    }