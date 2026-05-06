from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class HSEIncidentInvestigationCreate(BaseModel):
    incident_id: int

    report_number: Optional[str]

    incident_date: Optional[date]
    incident_time: Optional[time]
    reporting_date: Optional[date]

    location_details: Optional[str]
    pipeline_name_section: Optional[str]
    reported_by: Optional[str]

    # Incident Type
    is_leak: Optional[bool]
    is_spill: Optional[bool]
    is_fire: Optional[bool]
    is_explosion: Optional[bool]
    is_injury: Optional[bool]
    is_near_miss: Optional[bool]
    is_other: Optional[bool]

    # Severity
    severity_major: Optional[bool]
    severity_minor: Optional[bool]
    severity_near_miss: Optional[bool]
    severity_unsafe_act: Optional[bool]
    severity_unsafe_condition: Optional[bool]
    severity_high_potential_near_miss: Optional[bool]

    # Impact
    impact_on_people: Optional[str]
    impact_on_asset: Optional[str]
    environmental_impact: Optional[str]
    business_interruption: Optional[str]

    # Step 2
    immediate_action_taken: Optional[str]
    statutory_management_intimation: Optional[str]

    # Step 3
    incident_description: Optional[str]
    site_observations_evidence: Optional[str]

    immediate_causes: Optional[str]
    underlying_causes: Optional[str]
    root_causes: Optional[str]

    rca_tool_used: Optional[str]  # 5-Why / Fishbone / FTA

    # Step 4
    learning_recommendations: Optional[str]
    verification_closure: Optional[str]

    remarks_md: Optional[str]
    remarks_hse_head: Optional[str]
    remarks_station_incharge: Optional[str]

    allotted_to_name: Optional[str]
    allotted_to_designation: Optional[str]

    created_by: Optional[str]

    incident_id: int

    incident_date: Optional[date]
    incident_time: Optional[time]
    reporting_date: Optional[date]

    location_details: Optional[str]
    pipeline_name_section: Optional[str]
    reported_by: Optional[str]

    # Incident type
    is_leak: Optional[bool]
    is_spill: Optional[bool]
    is_fire: Optional[bool]
    is_explosion: Optional[bool]
    is_injury: Optional[bool]
    is_near_miss: Optional[bool]
    is_other: Optional[bool]

    # Severity
    severity_major: Optional[bool]
    severity_minor: Optional[bool]
    severity_near_miss: Optional[bool]
    severity_unsafe_act: Optional[bool]
    severity_unsafe_condition: Optional[bool]
    severity_high_potential_near_miss: Optional[bool]

    # Impact
    impact_on_people: Optional[str]
    impact_on_asset: Optional[str]
    environmental_impact: Optional[str]
    business_interruption: Optional[str]

    # Step 2
    immediate_action_taken: Optional[str]
    statutory_management_intimation: Optional[str]

    # Step 3
    incident_description: Optional[str]
    site_observations_evidence: Optional[str]
    immediate_causes: Optional[str]
    underlying_causes: Optional[str]
    root_causes: Optional[str]
    rca_tool_used: Optional[str]

    # Step 4
    learning_recommendations: Optional[str]
    verification_closure: Optional[str]

    remarks_md: Optional[str]
    remarks_hse_head: Optional[str]
    remarks_station_incharge: Optional[str]

    allotted_to_name: Optional[int]
    allotted_to_designation: Optional[str]

    created_by: Optional[str]
    status: Optional[str]



class HSEIncidentInvestigationUpdate(BaseModel):
    incident_id: int

    report_number: Optional[str]

    incident_date: Optional[date]
    incident_time: Optional[time]
    reporting_date: Optional[date]

    location_details: Optional[str]
    pipeline_name_section: Optional[str]
    reported_by: Optional[str]

    is_leak: Optional[bool]
    is_spill: Optional[bool]
    is_fire: Optional[bool]
    is_explosion: Optional[bool]
    is_injury: Optional[bool]
    is_near_miss: Optional[bool]
    is_other: Optional[bool]

    severity_major: Optional[bool]
    severity_minor: Optional[bool]
    severity_near_miss: Optional[bool]
    severity_unsafe_act: Optional[bool]
    severity_unsafe_condition: Optional[bool]
    severity_high_potential_near_miss: Optional[bool]

    impact_on_people: Optional[str]
    impact_on_asset: Optional[str]
    environmental_impact: Optional[str]
    business_interruption: Optional[str]

    immediate_action_taken: Optional[str]
    statutory_management_intimation: Optional[str]

    incident_description: Optional[str]
    site_observations_evidence: Optional[str]

    immediate_causes: Optional[str]
    underlying_causes: Optional[str]
    root_causes: Optional[str]

    rca_tool_used: Optional[str]

    learning_recommendations: Optional[str]
    verification_closure: Optional[str]

    remarks_md: Optional[str]
    remarks_hse_head: Optional[str]
    remarks_station_incharge: Optional[str]

    allotted_to_name: Optional[int]
    allotted_to_designation: Optional[str]

    updated_by: Optional[str]
    status: Optional[str]


