from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import date, time


class CompositeElectricalEnergizationPermitBase(BaseModel):
    composite_work_permit_id: Optional[int] = None

    work_permit_number: Optional[str] = None   # auto generated
    work_clearance_time: Optional[time] = None
    work_clearance_date: Optional[date] = None

    name_of_equipment_circuit: Optional[str] = None
    department_section_area: Optional[str] = None
    equipment_number_to_be_energized: Optional[str] = None
    cross_reference_of_other_permit: Optional[str] = None

    issuer_name: Optional[str] = None
    issuer_designation: Optional[str] = None
    issuer_signature: Optional[str] = None
    status: Optional[str] = None

    # ELECTRICAL certificate fields
    equipment_circuit_no: Optional[str] = None
    plant: Optional[str] = None
    work_clearance_from_time: Optional[time] = None
    work_clearance_from_date: Optional[date] = None
    energization_method: Optional[str] = None
    loto_tag_device_no: Optional[str] = None
    authorized_person_name: Optional[str] = None
    designation: Optional[str] = None
    signature: Optional[str] = None
    created_by: Optional[int] = None           # ← str to int

    @field_validator(
        "work_clearance_time",
        "work_clearance_date",
        "work_clearance_from_time",
        "work_clearance_from_date",
        mode="before"
    )
    @classmethod
    def empty_string_to_none(cls, v: Any) -> Any:
        if v == "":
            return None
        return v



class CompositeElectricalEnergizationPermitCreate(CompositeElectricalEnergizationPermitBase):
    created_by: int                            # ← required on create


class CompositeElectricalEnergizationPermitUpdate(CompositeElectricalEnergizationPermitBase):
    pass