from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time


class CompositeElectricalIsolationPermitSchema(BaseModel):
    ceip_id: int

    composite_work_permit_id: Optional[int]

    work_permit_number: Optional[str]
    type_of_permit: Optional[str] = "Electrical Isolation"

    work_clearance_time: Optional[time]
    work_clearance_date: Optional[date]

    cross_reference_of_other_permit: Optional[str]

    department_section_area: Optional[str]

    equipment_number_to_be_isolated: Optional[str]

    name_of_equipment_circuit: Optional[str]

    description_of_work: Optional[str]

    issuer_name: Optional[str]
    issuer_designation: Optional[str]
    issuer_signature: Optional[str]

    status: Optional[str]
    # ELECTRICAL certificate fields
    equipment_circuit_no: Optional[str] = None
    plant: Optional[str] = None
    work_clearance_from_time: Optional[time] = None
    work_clearance_from_date: Optional[date] = None
    isolation_method: Optional[str] = None
    loto_tag_device_no: Optional[str] = None
    authorized_person_name: Optional[str] = None
    designation: Optional[str] = None
    signature: Optional[str] = None

    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    station_name: Optional[str] = None    # ← add
    receiver_name: Optional[str] = None   # ← add

    class Config:
        orm_mode = True
