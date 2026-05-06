from decimal import Decimal

from pydantic import BaseModel
from pydantic import BaseModel
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class Material(BaseModel):
    id: Optional[int]
    outward_id: Optional[int]
    description: Optional[str]
    quantity: Optional[float]
    unit: Optional[str]
    returnable: Optional[bool]
    returnable_date: Optional[date] = None
    remarks: Optional[str]
    goods_photo: Optional[str]

    class Config:
        orm_mode = True

class OutwardGatePassItem(BaseModel):
    formtype:Optional[str]
    approver_id:Optional[int]
    outward_id: int
    gate_pass_no: str
    date_time: Optional[datetime]
    station: Optional[str]
    issuing_authority: Optional[str]
    department_contractor_name: Optional[str]
    purpose: Optional[str]
    address: Optional[str]
    material_taken_by: Optional[str]
    vehicle_no: Optional[str]
    driver_phone: Optional[str]
    initiator_name: Optional[str]
    approver_name: Optional[str]
    approved_at: Optional[date] = None
    status: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[datetime]
    created_by_name: Optional[str] = None
    updated_at: Optional[datetime]
    materials: List[Material] = []
 
class OutwardGatePassByStationResponse(BaseModel):
    status_code: int
    status_message: str
    data: List[OutwardGatePassItem] = []
    security: List[dict] = []  

class GatePassSummary(BaseModel):
    total_gate_pass_today: int
    pending_approvals: int
    returnable_pending: int
    total_inward_passes: int
    total_entries_today: int
    total_outward_passes: int

    class Config:
        orm_mode = True

class InwardMaterialDetailIn(BaseModel):
    description: str
    ordered_quantity: float
    received_quantity: float
    unit: str
    remarks: str

class InwardGatePassPhotoIn(BaseModel):
    uploaded_by: str

class InwardGatePassData(BaseModel):
    station: Optional[str] = None
    po_type: Optional[str] = None
    po_number: Optional[str] = None
    received_from: Optional[str] = None
    supplier_address: Optional[str] = None
    purpose: Optional[str] = None
    reference_document: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    security_guard: Optional[str] = None
    approver_name: Optional[str] = None
    status: Optional[str] = None
    approver_id: Optional[int] = None
    date_time: Optional[datetime]
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    uploaded_by: Optional[str] = None

class InwardGatePassIn(BaseModel):
    gate_pass_no: str
    station: str
    po_type: str
    po_number: str
    received_from: str
    supplier_address: str
    purpose: str
    reference_document: str
    vehicle_no: str
    driver_name: str
    driver_phone: str
    security_guard: str
    approver_name: str
    created_by: str
    updated_by: str
    materials: List[InwardMaterialDetailIn]
    uploaded_by: str 
  
class InwardMaterialDetailsRequest(BaseModel):
    inward_id: int
    description: str
    ordered_quantity: float
    received_quantity: float
    unit: str
    remarks: str

class InwardMaterialDetailsResponse(BaseModel):
    status_code: int
    status_message: str
    data: Union[dict, list]  

class InwardGatePassPhoto(BaseModel):
    vehicle_photo: Optional[str]
    delivery_personnel_photo: Optional[str]
    delivery_personnel_id_photo: Optional[str]
    goods_photo: Optional[str]
  
class InwardMaterial(BaseModel):
    material_id: int
    material_name: str
    quantity: int
 
    class Config:
        orm_mode = True

class InwardGatePassBase(BaseModel):
    station: Optional[str] = None
    po_type: Optional[str] = None
    po_number: Optional[str] = None
    received_from: Optional[str] = None
    supplier_address: Optional[str] = None
    purpose: Optional[str] = None
    reference_document: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    security_guard: Optional[str] = None
    approver_name: Optional[str] = None
    approver_id: Optional[int] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    uploaded_by: Optional[str] = None

class InwardGatePassCreate(InwardGatePassBase):
    station: Optional[str] = None
    po_type: Optional[str] = None
    po_number: Optional[str] = None
    received_from: Optional[str] = None
    supplier_address: Optional[str] = None
    purpose: Optional[str] = None
    reference_document: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    security_guard: Optional[str] = None
    approver_name: Optional[str] = None
    approver_id: Optional[int] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    uploaded_by: Optional[str] = None
    vehicle_photo: Optional[str] = None
    delivery_personnel_photo: Optional[str] = None
    delivery_personnel_id_photo: Optional[str] = None
    goods_photo: Optional[str] = None
    date_time: Optional[datetime] = None

class InwardGatePassCreateModel(BaseModel):
    station: Optional[str] = None
    po_type: Optional[str] = None
    po_number: Optional[str] = None
    received_from: Optional[str] = None
    supplier_address: Optional[str] = None
    purpose: Optional[str] = None
    reference_document: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    security_guard: Optional[str] = None
    approver_name: Optional[str] = None
    approver_id: Optional[int] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    uploaded_by: Optional[str] = None
    vehicle_photo: Optional[str] = None
    delivery_personnel_photo: Optional[str] = None
    delivery_personnel_id_photo: Optional[str] = None
    goods_photo: Optional[str] = None
    date_time: Optional[datetime] = None

class InwardGatePassUpdate(InwardGatePassBase):
    gate_pass_no: Optional[str] = None
    date_time: Optional[str] = None
    vehicle_photo: Optional[str] = None
    delivery_personnel_photo: Optional[str] = None
    delivery_personnel_id_photo: Optional[str] = None
    goods_photo: Optional[str] = None

# ── Request Model ─────────────────────────────────────────────────────────────
class UpdateReturnableGatePassRequest(BaseModel):
    outward_id:   int
    returnable_id: int        
    approved_by:  Optional[str] = None
    reviewer_id:  Optional[int] = None
    status:       str
    date_time:   Optional[datetime] = None
    updated_by:   str
  
class APIResponse(BaseModel):
    status_code: int
    status_message: str
    data: Any
 
class InwardGatePassResponse(InwardGatePassBase):
    inward_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    photos: List[InwardGatePassPhoto] = []
    materials: List[InwardMaterial] = []
 
    class Config:
        orm_mode = True
 
class OutwardMaterialDetailsRequest(BaseModel):
    outward_id: int
    description: str
    quantity: float
    unit: str
    returnable: bool
    returnable_date: Optional[date] = None
    remarks: Optional[str] = None
 
class OutwardMaterialDetailsResponse(BaseModel):
    status_code: int
    status_message: str
    data: Optional[dict]

class OutwardGatePassByUserRequest(BaseModel):
    user_id: int
 
class GatePassPhoto(BaseModel):
    id: int
    vehicle_photo: Optional[str]
    delivery_personnel_photo: Optional[str]
    delivery_personnel_id_photo:Optional[str]
    goods_photo: Optional[str]
    uploaded_by: str
    uploaded_at: datetime

class InwardMaterialDetail(BaseModel):
    id: int
    inward_id: int
    material_name: str
    qty: int
    unit: str

class OutwardMaterialDetail(BaseModel):
    id: int
    outward_id: int
    material_name: str
    qty: int
    unit: str

class InwardGatePassFull(BaseModel):
    type: str
    form: dict
    materials: List[InwardMaterialDetail] | list
    photos: List[GatePassPhoto] | list

class OutwardGatePassFull(BaseModel):
    type: str
    form: dict
    materials: List[OutwardMaterialDetail] | list
    photos: List[GatePassPhoto] | list

class ReturnableGatePassFull(BaseModel):
    type: str
    form: dict
    materials: list
    photos: List[GatePassPhoto] | list

class GatePassDetailsResponse(BaseModel):
    status_code: int
    status_message: str
    data: Union[Dict[str, Any], List[Any], None] = None

    model_config = {
        "from_attributes": True
    }

class AllGatePassListResponse(BaseModel):
    status_code: int
    status_message: str
    data: Union[Dict[str, Any], List[Any], None] = None

    model_config = {
        "from_attributes": True
    }

class OutwardGatePassCreate(BaseModel):
    approver_id: int
    station: str
    issuing_authority: str
    department_contractor_name: str
    purpose: str
    address: str
    material_taken_by: str
    vehicle_no: str
    driver_phone: str
    initiator_name: str
    approver_name: str
    created_by: str
    status: str                         # <-- REQUIRED FIELD ADDED
    vehicle_photo: Optional[str] | None = None
    delivery_personnel_photo: Optional[str] | None = None
    delivery_personnel_id_photo: Optional[str] | None = None
    goods_photo: Optional[str] | None = None
 
class OutwardGatePassUpdate(BaseModel):
    vehicle_no: str
    driver_phone: str
    purpose: str
    updated_by: str
    approved_at: Optional[datetime] = None  
    status: Optional[str] = None   
    approver_id:Optional[int] = None    

class Photo(BaseModel):
    id: Optional[int]
    vehicle_photo: Optional[str]
    delivery_personnel_photo: Optional[str]
    delivery_personnel_id_photo: Optional[str]
    goods_photo: Optional[str]
    uploaded_by: Optional[str]
    uploaded_at: Optional[datetime]

    class Config:
        orm_mode = True

class Outward(BaseModel):
    outward_id: int
    gate_pass_no: str
    date_time: datetime
    station: str
    issuing_authority: str
    department_contractor_name: str
    purpose: str
    address: str
    material_taken_by: str
    vehicle_no: str
    driver_phone: str
    initiator_name: str
    approver_name: str
    status: str
    created_by: str
    updated_by: str
    updated_by_name: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class OutwardData(BaseModel):
    outward: Outward
    materials: List[Material] = []   
    photos: List[Photo] = []

    class Config:
        orm_mode = True

class OutwardResponse(BaseModel):
    status: str
    data: OutwardData

    class Config:
        orm_mode = True

class MaterialReturnItem(BaseModel):
    description: str
    returned_quantity: float
    unit: str
    condition: str
    remarks: str
    goods_photo: str

class ReturnableGatePassReturnRequest(BaseModel):
    returnable_gate_pass_no: str
    materials: List[MaterialReturnItem]
    vehicle_photo: Optional[str]
    delivery_personnel_photo: Optional[str]
    delivery_personnel_id_photo: Optional[str]
    goods_photo: Optional[str]
    uploaded_by: str

class ReturnableGatePassRequest(BaseModel):
    outward_id: int
    created_by: str
    approver_name: str
    reviewer_id: Optional[int] = None
    gate_pass_no: Optional[str] = None
    station: Optional[str] = None
    department_contractor_name: Optional[str] = None
    purpose: Optional[str] = None
    address: Optional[str] = None
    material_taken_by: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_phone: Optional[str] = None

class ReturnableGatePassTrackerRequest(BaseModel):
    outward_id: int
    created_by: str
    approver_name: str

class ReturnableMaterialDetailBase(BaseModel):
    returnable_id: int
    description: str
    actual_quantity: float
    received_quantity: float
    unit: str
    condition: str
    remarks: str
    goods_photo: str
    returned_goods_photo: str
 
class ReturnableMaterialDetailCreate(ReturnableMaterialDetailBase):
    pass
 
class ReturnableMaterialDetailUpdate(ReturnableMaterialDetailBase):
    pass
 
class ReturnableMaterialDetailResponse(ReturnableMaterialDetailBase):
    id: int
 
    class Config:
        orm_mode = True
 
class MaterialSchema(BaseModel):
    description: str
    actual_quantity: int
    received_quantity: int
    unit: str
    remarks: Optional[str]
    goods_photo: Optional[str]

class ReturnableGatePassData(BaseModel):
    returnable_id: int
    outward_id: int
    returnable_gate_pass_no: str
    approved_by: Optional[str] = None    
    date_time: datetime
    status: str
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime

class ReturnableGatePassData(BaseModel):
    returnable_id: int
    outward_id: int
    returnable_gate_pass_no: str
    approved_by: Optional[str] = None
    reviewer_id: Optional[int] = None
    date_time: datetime
    status: str
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime
    gate_pass_no: Optional[str] = None
    date_time_ret: Optional[datetime] = None
    station: Optional[str] = None
    department_contractor_name: Optional[str] = None
    purpose: Optional[str] = None
    address: Optional[str] = None
    material_taken_by: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_phone: Optional[str] = None

class ReturnableGatePassResponse(BaseModel):
    status: str
    message: str
    data: Optional[ReturnableGatePassData]
 
class OutwardDetails(BaseModel):
    gate_pass_no: Optional[str]
    date_time: Optional[str]
    station: Optional[str]
    issuing_authority: Optional[str]
    department_contractor_name: Optional[str]
    purpose: Optional[str]
    address: Optional[str]
    material_taken_by: Optional[str]
    vehicle_no: Optional[str]
    driver_phone: Optional[str]
    initiator_name: Optional[str]
    approver_name: Optional[str]

class ReturnableGatePass(BaseModel):
    returnable_id: int
    returnable_gate_pass_no: str
    outward_id: int
    approved_by: Optional[str]
    date_time: Optional[str]
    status: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    outward_details: Optional[OutwardDetails]

class ReturnableGatePassResponses(BaseModel):
    status_code: int
    status_message: str
    data: List[Any]
    security: List[Any]

class OutwardDetails(BaseModel):
    gate_pass_no: Optional[str]
    date_time: Optional[str]
    station: Optional[str]
    issuing_authority: Optional[str]
    department_contractor_name: Optional[str]
    purpose: Optional[str]
    address: Optional[str]
    material_taken_by: Optional[str]
    vehicle_no: Optional[str]
    driver_phone: Optional[str]
    initiator_name: Optional[str]
    approver_name: Optional[str]

class ReturnableGatePass(BaseModel):
    returnable_id: int
    returnable_gate_pass_no: str
    outward_id: int
    approved_by: Optional[str]
    date_time: Optional[str]
    status: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    outward_details: Optional[OutwardDetails]

class InwardMaterialDetailSchema(BaseModel):
    id: int
    inward_id: int
    material_name: str
    qty: int
    unit: str


from pydantic import BaseModel
from typing import Optional, Any

class AssetEntitlementResponse(BaseModel):
    category: str
    item_type: str
    total_entitlement_limit: Decimal
    amount_utilized: Decimal
    balance_available: Decimal
    eligibility: str
    can_apply: bool
    last_claim_date: Optional[date]
    next_eligible_date: Optional[date]
    policy_message: str

    class Config:
        from_attributes = True

class FurnitureDashboard(BaseModel):
    utility_decorative: AssetEntitlementResponse
    office: AssetEntitlementResponse

class AssetDashboardResponse(BaseModel):
    user_id: int
    dashboard: dict  # or make it a typed model if you prefer strict typing












































