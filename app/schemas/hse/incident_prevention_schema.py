from pydantic import BaseModel
from typing import Optional
from datetime import date


class IncidentPreventionBase(BaseModel):
    incident_id: int

    # ================= COMMON =================
    was_incident_avoidable: Optional[bool] = None

    avoid_better_supervision: Optional[bool] = None
    avoid_imparting_training: Optional[bool] = None
    avoid_work_permit_system: Optional[bool] = None
    avoid_better_equipment: Optional[bool] = None
    avoid_maintenance_procedure: Optional[bool] = None
    avoid_other_information: Optional[bool] = None

    avoid_operating_procedure: Optional[bool] = None
    avoid_proper_planning_time: Optional[bool] = None
    avoid_ppe: Optional[bool] = None
    avoid_management_control: Optional[bool] = None
    avoid_inspection_testing: Optional[bool] = None

    # ================= MINOR (MAIN) =================
    minor_prepared_by_name: Optional[str] = None
    minor_prepared_by_designation: Optional[str] = None
    minor_recommendations: Optional[str] = None
    minor_engineer_corrective_actions_taken: Optional[str] = None
    minor_prepared_by_corrective_action: Optional[str] = None
    minor_corrective_actions: Optional[str] = None
    minor_prepared_by_remarks: Optional[str] = None
    minor_preventive_action_taken: Optional[str] = None

    # ✅ ENGINEER ASSIGNMENT (matches DB exactly)
    minor_allotted_responsible_id: Optional[int] = None
    minor_allotted_engineer_id: Optional[int] = None
    minor_responsible_engineer_name: Optional[str] = None
    minor_responsible_engineer_designation: Optional[str] = None

    # ================= MINOR APPROVAL =================
    minor_approved_by_name: Optional[str] = None
    minor_approved_by_station_incharge: Optional[str] = None
    minor_approved_by_remarks: Optional[str] = None

    # ================= MINOR WORKFLOW =================
    minor_sic_name: Optional[str] = None
    minor_sic_updated_date: Optional[date] = None

    # ⚠️ workflow engineer (single-t — DB column name)
    minor_alloted_engineer_name: Optional[str] = None
    minor_alloted_eng_updated_date: Optional[date] = None

    minor_final_approve_name: Optional[str] = None
    minor_final_approved_date: Optional[date] = None

    # ================= MINOR ATTACHMENTS =================
    # minor_evidence_document_path is handled via UploadFile in the router.
    # This field stores a JSON list of paths for multiple attachments.
    minor_evidence_documents_multi: Optional[str] = None   # ✅ NEW

    # ================= MAJOR =================
    major_prepared_by_name: Optional[str] = None
    major_prepared_by_designation: Optional[str] = None
    major_immediate_actions_taken: Optional[str] = None
    major_recommendations: Optional[str] = None
    major_prepared_by_remarks_si: Optional[str] = None
    major_hse_head_remarks: Optional[str] = None

    # ================= MAJOR ATTACHMENTS =================
    # major_evidence_document_path is handled via UploadFile in the router.
    # This field stores a JSON list of paths for multiple attachments.
    major_evidence_documents_multi: Optional[str] = None   # ✅ NEW

    # ================= MAJOR WORKFLOW =================
    major_team_leader_by: Optional[str] = None
    major_team_leader_date: Optional[date] = None

    major_team_acknowledged_by: Optional[str] = None
    major_team_acknowledged_date: Optional[date] = None

    major_report_filled_by: Optional[str] = None
    major_report_filled_date: Optional[date] = None

    major_investigation_ack_by: Optional[str] = None
    major_investigation_ack_date: Optional[date] = None

    major_safety_officer_by: Optional[str] = None
    major_safety_officer_date: Optional[date] = None

    major_md_review_by: Optional[str] = None
    major_md_review_date: Optional[date] = None

    major_hse_review_by: Optional[str] = None
    major_hse_review_date: Optional[date] = None

    major_capa_filled_by: Optional[str] = None
    major_capa_filled_date: Optional[date] = None

    major_hse_capa_review_by: Optional[str] = None
    major_hse_capa_review_date: Optional[date] = None

    major_closure_by: Optional[str] = None
    major_closure_date: Optional[date] = None

    # ================= STATUS =================
    status: Optional[str] = None


# ================= CREATE =================
class IncidentPreventionCreate(IncidentPreventionBase):
    created_by: Optional[int] = None


# ================= UPDATE =================
class IncidentPreventionUpdate(IncidentPreventionBase):
    updated_by: Optional[int] = None