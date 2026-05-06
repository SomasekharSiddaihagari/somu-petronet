from pydantic import BaseModel
from typing import Optional, Literal



# =========================
# CREATE
# =========================
class IncidentImpactAssessmentCreate(BaseModel):
    incident_id: int   # FK (mandatory)

    fatalities_employees: Optional[int]
    fatalities_contractor: Optional[int]
    fatalities_others: Optional[int]

    injuries_employees: Optional[int]
    injuries_contractor: Optional[int]
    injuries_others: Optional[int]

    man_hours_lost_employees: Optional[int]
    man_hours_lost_contractor: Optional[int]
    man_hours_lost_others: Optional[int]

    direct_loss_details: Optional[str]
    indirect_loss_details: Optional[str]

    facility_status: Optional[str]


    brief_incident_description: Optional[str]
    similar_incident_past: Optional[str]

    status: Optional[str]
    created_by: Optional[str]


# =========================
# UPDATE (FULL)
# =========================
class IncidentImpactAssessmentUpdate(BaseModel):
    fatalities_employees: Optional[int]
    fatalities_contractor: Optional[int]
    fatalities_others: Optional[int]

    injuries_employees: Optional[int]
    injuries_contractor: Optional[int]
    injuries_others: Optional[int]

    man_hours_lost_employees: Optional[int]
    man_hours_lost_contractor: Optional[int]
    man_hours_lost_others: Optional[int]

    direct_loss_details: Optional[str]
    indirect_loss_details: Optional[str]

    facility_status: Optional[str]


    brief_incident_description: Optional[str]
    similar_incident_past: Optional[str]

    status: Optional[str]
    updated_by: Optional[str]
