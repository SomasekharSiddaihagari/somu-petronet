from fastapi import APIRouter, Depends
from app.crud.claim.allowance_validation_crud import validate_admission_claim, validate_packing_charges
from app.database import get_db
from app.models.claim.data_card_reimbursement import DataCardReimbursement
from app.models.claim.mobile_bill_reimbursement import MobileBillReimbursement
from app.schemas.claim.allowance_validation_schema import AdmissionClaimRequest, AdmissionClaimResponse, PackingChargesRequest, PackingChargesResponse
from app.schemas.claim.validation_schema import (
    DataCardValidateRequest,
    DataCardValidateResponse
)
from app.crud.claim.validation_crud import validate_data_card
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/api",
    tags=["Validation API's"]
)


@router.post("/data-card/validate", response_model=DataCardValidateResponse)
def validate_data_card_claim(
    payload: DataCardValidateRequest,
    db: Session = Depends(get_db),
):
    # -------------------------------------------------
    # 🔒 SAME USER + SAME MONTH CHECK
    # -------------------------------------------------
    existing_claim = (
        db.query(DataCardReimbursement)
        .filter(
            DataCardReimbursement.created_by == payload.user_id,
            DataCardReimbursement.claim_month == payload.claim_month
        )
        .first()
    )

    if existing_claim:
        return DataCardValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=[
                f"Data Card reimbursement already claimed for {payload.claim_month}"
            ],
            message="Duplicate Data Card claim not allowed for same month"
        )

    # -------------------------------------------------
    # POLICY VALIDATION
    # -------------------------------------------------
    errors, bill_total, monthly_limit = validate_data_card(payload,db)

    if errors:
        return DataCardValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=errors,
            message="Data Card reimbursement validation failed"
        )

    return DataCardValidateResponse(
        status="VALID",
        eligible=True,
        bill_amount_total=bill_total,
        monthly_limit=monthly_limit,
        message="Data Card reimbursement validated successfully"
    )






from fastapi import APIRouter
from app.schemas.claim.validation_schema import (
    FurnitureRMValidateRequest,
    FurnitureRMValidateResponse
)
from app.crud.claim.validation_crud import validate_furniture_rm




@router.post("/furniture-rm/validate", response_model=FurnitureRMValidateResponse)
def validate_furniture_rm_claim(
    payload: FurnitureRMValidateRequest,
    db: Session = Depends(get_db)
):
    errors = validate_furniture_rm(payload, db)

    if errors:
        return FurnitureRMValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=errors,
            message="Furniture R&M reimbursement validation failed"
        )

    return FurnitureRMValidateResponse(
        status="VALID",
        eligible=True,
        message="Furniture R&M reimbursement validated successfully"
    )




from fastapi import APIRouter
from app.schemas.claim.validation_schema import (
    LaptopMaintenanceValidateRequest,
    LaptopMaintenanceValidateResponse
)
from app.crud.claim.validation_crud import validate_laptop_maintenance




@router.post(
    "/laptop-maintenance/validate",
    response_model=LaptopMaintenanceValidateResponse
    )
def validate_laptop_maintenance_claim(
    payload: LaptopMaintenanceValidateRequest,
    db: Session = Depends(get_db)
):
    errors, annual_limit, eligible_amount = validate_laptop_maintenance(payload, db)

    if errors:
        return LaptopMaintenanceValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=errors,
            message="Laptop maintenance reimbursement validation failed"
        )

    return LaptopMaintenanceValidateResponse(
        status="VALID",
        eligible=True,
        annual_limit=annual_limit,
        eligible_amount=eligible_amount,
        message="Laptop maintenance reimbursement validated successfully"
    )

from fastapi import APIRouter
from app.schemas.claim.validation_schema import (
    MobileBillValidateRequest,
    MobileBillValidateResponse
)
from app.crud.claim.validation_crud import validate_mobile_bill




# @router.post("/mobile-bill/validate", response_model=MobileBillValidateResponse)
# def validate_mobile_bill_claim(payload: MobileBillValidateRequest):

#     errors, total_amount, monthly_limit = validate_mobile_bill(payload)

#     if errors:
#         return MobileBillValidateResponse(
#             status="REJECTED",
#             eligible=False,
#             errors=errors,
#             message="Mobile bill reimbursement validation failed"
#         )

#     return MobileBillValidateResponse(
#         status="VALID",
#         eligible=True,
#         total_claimed_amount=total_amount,
#         monthly_limit=monthly_limit,
#         message="Mobile bill reimbursement validated successfully"
#     )
    
from sqlalchemy import exists

from sqlalchemy import exists

@router.post("/mobile-bill/validate", response_model=MobileBillValidateResponse)
def validate_mobile_bill_claim(
    payload: MobileBillValidateRequest,
    db: Session = Depends(get_db),
):
    # -------------------------------------------------
    # 🔒 DUPLICATE CHECK (user + month)
    # -------------------------------------------------
    already_claimed = db.query(
        exists().where(
            (MobileBillReimbursement.created_by == payload.user_id) &
            (MobileBillReimbursement.bill_month_year == payload.bill_month_year)
        )
    ).scalar()

    if already_claimed:
        return MobileBillValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=[
                f"Mobile Bill already claimed for {payload.bill_month_year}"
            ],
            message="User cannot claim Mobile Bill twice in the same month"
        )

    # -------------------------------------------------
    # ✅ CALCULATION (THIS WAS MISSING)
    # -------------------------------------------------
    errors, total_amount, monthly_limit = validate_mobile_bill(payload)

    if errors:
        return MobileBillValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=errors,
            message="Mobile bill reimbursement validation failed"
        )

    return MobileBillValidateResponse(
        status="VALID",
        eligible=True,
        total_claimed_amount=total_amount,   # ✅ 650
        monthly_limit=monthly_limit,         # ✅ 700
        message="Mobile bill reimbursement validated successfully"
    )





from fastapi import APIRouter
from app.schemas.claim.validation_schema import (
    OutOfPocketValidateRequest,
    OutOfPocketValidateResponse
)
from app.crud.claim.validation_crud import validate_out_of_pocket



from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db


@router.post("/out-of-pocket/validate", response_model=OutOfPocketValidateResponse)
def validate_out_of_pocket_claim(
    payload: OutOfPocketValidateRequest,
    db: Session = Depends(get_db),
):
    errors, total_claims, total_amount = validate_out_of_pocket(db, payload)

    if errors:
        return OutOfPocketValidateResponse(
            status="REJECTED",
            eligible=False,
            errors=errors,
            message="Out-of-Pocket claim validation failed"
        )

    return OutOfPocketValidateResponse(
        status="VALID",
        eligible=True,
        total_claims=total_claims,
        total_amount=total_amount,
        message="Out-of-Pocket claim validated successfully"
    )



from fastapi import APIRouter
from app.schemas.claim.validation_schema import VehicleCMValidateRequest
from app.crud.claim.validation_crud import validate_vehicle_cm



@router.post("/vehicle-cm/validate")
def validate_vehicle_cm_claim(
    payload: VehicleCMValidateRequest,
    db: Session = Depends(get_db),
):
    errors, data, flags = validate_vehicle_cm(payload, db)

    if errors:
        return {
            "status": "REJECTED",
            "eligible": False,
            "errors": errors,
            "flags": flags,   # 🔥 ALWAYS RETURN FLAGS
            "message": "Vehicle Conveyance & Maintenance validation failed"
        }

    return {
        "status": "VALID",
        "eligible": True,
        "calculated_entitlement": data,
        "flags": flags,      # 🔥 ALSO RETURN FLAGS ON SUCCESS
        "message": "Vehicle Conveyance & Maintenance validated successfully"
    }

# -------------------------

# Packing Charges API

# -------------------------

@router.post(

    "/validate/packing-charges",

    response_model=PackingChargesResponse

)

def packing_charges_api(payload: PackingChargesRequest):

    return validate_packing_charges(

        payload.grade,

        payload.amount_claimed

    )
 
 
# -------------------------

# Admission Children API

# -------------------------

from fastapi import Depends
from sqlalchemy.orm import Session
@router.post(
    "/validate/admission-children",
    response_model=AdmissionClaimResponse
)
def admission_claim_api(
    payload: AdmissionClaimRequest,
    db: Session = Depends(get_db)
    ):
    return validate_admission_claim(
    user_id=payload.user_id,
    station_id=payload.station_id,
    city=payload.city,
    children=payload.children,
    db=db
)


 