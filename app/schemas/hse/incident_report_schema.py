from pydantic import BaseModel
from datetime import date, time
from typing import Optional, Literal


# =========================
# CREATE SCHEMA
# =========================
class IncidentReportCreate(BaseModel):
    category: Literal["Major", "Minor"]   # Dropdown
    sector: Optional[str]

    location: Optional[str]
    incident_no_during_year: Optional[str]

    date_of_incident: Optional[date]
    time_of_incident: Optional[time]

    incident_type: Optional[str]
    fire_incident: Optional[str]

    report_type: Optional[str]
    duration_of_fire: Optional[str]

    loss_of_life_injury: Optional[bool]
    electrocution: Optional[bool]
    slip_trip: Optional[bool]
    fire: Optional[bool]
    fall_from_height: Optional[bool]
    leak_spill: Optional[bool]
    explosion: Optional[bool]
    inhalation_of_gas: Optional[bool]
    blowout: Optional[bool]
    driving: Optional[bool]

    others: Optional[bool]
    others_text: Optional[str]

        # ===== Minor Workflow =====
    minor_sic_name: Optional[str]
    minor_sic_updated_date: Optional[date]

    minor_alloted_engineer_name: Optional[str]
    minor_alloted_eng_updated_date: Optional[date]

    minor_final_approve_name: Optional[str]
    minor_final_approved_date: Optional[date]

    # ===== Major Workflow =====
    major_team_leader_by: Optional[str]
    major_team_leader_date: Optional[date]

    major_team_acknowledged_by: Optional[str]
    major_team_acknowledged_date: Optional[date]

    major_report_filled_by: Optional[str]
    major_report_filled_date: Optional[date]

    major_investigation_ack_by: Optional[str]
    major_investigation_ack_date: Optional[date]

    major_safety_officer_by: Optional[str]
    major_safety_officer_date: Optional[date]

    major_md_review_by: Optional[str]
    major_md_review_date: Optional[date]

    major_hse_review_by: Optional[str]
    major_hse_review_date: Optional[date]

    major_capa_filled_by: Optional[str]
    major_capa_filled_date: Optional[date]

    major_hse_capa_review_by: Optional[str]
    major_hse_capa_review_date: Optional[date]

    major_closure_by: Optional[str]
    major_closure_date: Optional[date]


    incident_location_detail: Optional[str]
    plant_shutdown: Optional[bool]
    station: Optional[int]
    status: Optional[str]
    created_by: Optional[str]


# =========================
# UPDATE SCHEMA (FULL)
# =========================
class IncidentReportUpdate(BaseModel):
    category: Optional[Literal["Major", "Minor"]]
    sector: Optional[str]

    location: Optional[str]
    incident_no_during_year: Optional[str]

    date_of_incident: Optional[date]
    time_of_incident: Optional[time]

    incident_type: Optional[str]
    fire_incident: Optional[str]

    report_type: Optional[str]
    duration_of_fire: Optional[str]

        # ===== Minor Workflow =====
    minor_sic_name: Optional[str]
    minor_sic_updated_date: Optional[date]

    minor_alloted_engineer_name: Optional[str]
    minor_alloted_eng_updated_date: Optional[date]

    minor_final_approve_name: Optional[str]
    minor_final_approved_date: Optional[date]

    # ===== Major Workflow =====
    major_team_leader_by: Optional[str]
    major_team_leader_date: Optional[date]

    major_team_acknowledged_by: Optional[str]
    major_team_acknowledged_date: Optional[date]

    major_report_filled_by: Optional[str]
    major_report_filled_date: Optional[date]

    major_investigation_ack_by: Optional[str]
    major_investigation_ack_date: Optional[date]

    major_safety_officer_by: Optional[str]
    major_safety_officer_date: Optional[date]

    major_md_review_by: Optional[str]
    major_md_review_date: Optional[date]

    major_hse_review_by: Optional[str]
    major_hse_review_date: Optional[date]

    major_capa_filled_by: Optional[str]
    major_capa_filled_date: Optional[date]

    major_hse_capa_review_by: Optional[str]
    major_hse_capa_review_date: Optional[date]

    major_closure_by: Optional[str]
    major_closure_date: Optional[date]


    loss_of_life_injury: Optional[bool]
    electrocution: Optional[bool]
    slip_trip: Optional[bool]
    fire: Optional[bool]
    fall_from_height: Optional[bool]
    leak_spill: Optional[bool]
    explosion: Optional[bool]
    inhalation_of_gas: Optional[bool]
    blowout: Optional[bool]
    driving: Optional[bool]

    others: Optional[bool]
    others_text: Optional[str]

    incident_location_detail: Optional[str]
    plant_shutdown: Optional[bool]

    status: Optional[str]
    updated_by: Optional[str]


# =========================
# RESPONSE SCHEMA
# =========================
class IncidentReportResponse(BaseModel):
    incident_id: int
    category: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True
