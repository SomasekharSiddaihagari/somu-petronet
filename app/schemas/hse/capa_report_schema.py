from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class CapaReportBase(BaseModel):
    incident_id: int

    # Header
    format_no: Optional[str] = None
    revision_date: Optional[str] = None
    report_no: Optional[str] = None

    # Study
    department: Optional[str] = None
    start_date: Optional[date] = None
    team_or_capa_study: Optional[str] = None
    planned_completion_date: Optional[date] = None
    reference_no: Optional[str] = None
    hse_head_id: Optional[int] = None

    # Problem
    problem_description: Optional[str] = None

    # Correction
    correction_action: Optional[str] = None
    correction_target_date: Optional[date] = None
    correction_actual_date: Optional[date] = None

    # Root Cause
    root_cause_analysis: Optional[str] = None

    # Corrective
    corrective_action: Optional[str] = None
    corrective_target_date: Optional[date] = None
    corrective_actual_date: Optional[date] = None

    # Preventive
    preventive_action: Optional[str] = None
    preventive_target_date: Optional[date] = None
    preventive_actual_date: Optional[date] = None

    # Evidence
    evidence_file_name: Optional[str] = None
    evidence_file_path: Optional[str] = None
    evidence_file_type: Optional[str] = None

    # Authorization
    prepared_by_name: Optional[str] = None
    prepared_by_designation: Optional[str] = None
    approved_by_name: Optional[str] = None
    approved_by_designation: Optional[str] = None

    remarks: Optional[str] = None
    status: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class CapaReportCreate(CapaReportBase):
    pass


class CapaReportUpdate(BaseModel):
    format_no: Optional[str] = None
    revision_date: Optional[str] = None
    report_no: Optional[str] = None
    department: Optional[str] = None
    start_date: Optional[date] = None
    team_or_capa_study: Optional[str] = None
    planned_completion_date: Optional[date] = None
    reference_no: Optional[str] = None
    hse_head_id: Optional[int] = None

    problem_description: Optional[str] = None
    correction_action: Optional[str] = None
    correction_target_date: Optional[date] = None
    correction_actual_date: Optional[date] = None

    root_cause_analysis: Optional[str] = None

    corrective_action: Optional[str] = None
    corrective_target_date: Optional[date] = None
    corrective_actual_date: Optional[date] = None

    preventive_action: Optional[str] = None
    preventive_target_date: Optional[date] = None
    preventive_actual_date: Optional[date] = None

    evidence_file_name: Optional[str] = None
    evidence_file_path: Optional[str] = None
    evidence_file_type: Optional[str] = None

    prepared_by_name: Optional[str] = None
    prepared_by_designation: Optional[str] = None
    approved_by_name: Optional[str] = None
    approved_by_designation: Optional[str] = None

    remarks: Optional[str] = None
    status: Optional[str] = None