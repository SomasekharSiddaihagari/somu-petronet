# app/routers/hse/incident_investigation_master_router.py
from fastapi import (
    APIRouter, BackgroundTasks, Depends, Form, File,
    UploadFile, HTTPException
)
from sqlalchemy.orm import Session
from typing import List

from app.crud.hse.hse_incident_investigation_team_crud import get_full_investigation
from app.crud.hse.hse_major_notification import notify_engineer_allotted, notify_investigation_report_filled
from app.database import get_db
from app.crud.hse.hse_incident_investigation_master_crud import (
    create_investigation,
    update_investigation,
    get_all_investigations,
    get_investigation_by_id
)
from app.models.hse.hse_incident_investigation_master import HSEIncidentInvestigationMaster

router = APIRouter(
    prefix="/hse/incident-investigation",
    tags=["HSE - Incident Investigation Master"]
)


@router.post("/create")
def create_hiim(
    incident_id: int = Form(...),
    report_number: str | None = Form(None),
    incident_date: str | None = Form(None),
    incident_time: str | None = Form(None),
    reporting_date: str | None = Form(None),

    location_details: str | None = Form(None),
    pipeline_name_section: str | None = Form(None),
    reported_by: str | None = Form(None),

    is_leak: bool | None = Form(None),
    is_spill: bool | None = Form(None),
    is_fire: bool | None = Form(None),
    is_explosion: bool | None = Form(None),
    is_injury: bool | None = Form(None),
    is_near_miss: bool | None = Form(None),
    is_other: bool | None = Form(None),

    severity_major: bool | None = Form(None),
    severity_minor: bool | None = Form(None),
    severity_near_miss: bool | None = Form(None),
    severity_unsafe_act: bool | None = Form(None),
    severity_unsafe_condition: bool | None = Form(None),
    severity_high_potential_near_miss: bool | None = Form(None),

    impact_on_people: str | None = Form(None),
    impact_on_asset: str | None = Form(None),
    environmental_impact: str | None = Form(None),
    business_interruption: str | None = Form(None),

    immediate_action_taken: str | None = Form(None),
    statutory_management_intimation: str | None = Form(None),

    incident_description: str | None = Form(None),
    site_observations_evidence: str | None = Form(None),

    immediate_causes: str | None = Form(None),
    underlying_causes: str | None = Form(None),
    root_causes: str | None = Form(None),

    rca_tool_used: str | None = Form(None),

    learning_recommendations: str | None = Form(None),
    verification_closure: str | None = Form(None),

    remarks_md: str | None = Form(None),
    remarks_hse_head: str | None = Form(None),
    remarks_station_incharge: str | None = Form(None),

    allotted_to_name: int | None = Form(None),
    allotted_to_designation: str | None = Form(None),

    created_by: str | None = Form(None),
    status: str | None = Form(None),

    annexure_files: List[UploadFile] | None = File(None),
    db: Session = Depends(get_db)
):
    payload = locals()
    payload.pop("db")
    payload.pop("annexure_files")

    return create_investigation(db, payload, annexure_files)


# @router.put("/update/{hiim_id}")
# async def update_hiim(
#     hiim_id: int,

#     report_number: str | None = Form(None),
#     incident_date: str | None = Form(None),
#     incident_time: str | None = Form(None),
#     reporting_date: str | None = Form(None),

#     location_details: str | None = Form(None),
#     pipeline_name_section: str | None = Form(None),
#     reported_by: str | None = Form(None),

#     is_leak: bool | None = Form(None),
#     is_spill: bool | None = Form(None),
#     is_fire: bool | None = Form(None),
#     is_explosion: bool | None = Form(None),
#     is_injury: bool | None = Form(None),
#     is_near_miss: bool | None = Form(None),
#     is_other: bool | None = Form(None),

#     severity_major: bool | None = Form(None),
#     severity_minor: bool | None = Form(None),
#     severity_near_miss: bool | None = Form(None),
#     severity_unsafe_act: bool | None = Form(None),
#     severity_unsafe_condition: bool | None = Form(None),
#     severity_high_potential_near_miss: bool | None = Form(None),

#     impact_on_people: str | None = Form(None),
#     impact_on_asset: str | None = Form(None),
#     environmental_impact: str | None = Form(None),
#     business_interruption: str | None = Form(None),

#     immediate_action_taken: str | None = Form(None),
#     statutory_management_intimation: str | None = Form(None),

#     incident_description: str | None = Form(None),
#     site_observations_evidence: str | None = Form(None),

#     immediate_causes: str | None = Form(None),
#     underlying_causes: str | None = Form(None),
#     root_causes: str | None = Form(None),

#     rca_tool_used: str | None = Form(None),

#     learning_recommendations: str | None = Form(None),
#     verification_closure: str | None = Form(None),

#     remarks_md: str | None = Form(None),
#     remarks_hse_head: str | None = Form(None),
#     remarks_station_incharge: str | None = Form(None),

#     allotted_to_name: int | None = Form(None),
#     allotted_to_designation: str | None = Form(None),

#     updated_by: str | None = Form(None),
#     status: str | None = Form(None),


#     annexure_files: List[UploadFile] | None = File(None),
#     background_tasks: BackgroundTasks = BackgroundTasks(),
#     db: Session = Depends(get_db)
# ):
#     payload = {
#         "report_number": report_number,
#         "incident_date": incident_date,
#         "incident_time": incident_time,
#         "reporting_date": reporting_date,

#         "location_details": location_details,
#         "pipeline_name_section": pipeline_name_section,
#         "reported_by": reported_by,

#         "is_leak": is_leak,
#         "is_spill": is_spill,
#         "is_fire": is_fire,
#         "is_explosion": is_explosion,
#         "is_injury": is_injury,
#         "is_near_miss": is_near_miss,
#         "is_other": is_other,

#         "severity_major": severity_major,
#         "severity_minor": severity_minor,
#         "severity_near_miss": severity_near_miss,
#         "severity_unsafe_act": severity_unsafe_act,
#         "severity_unsafe_condition": severity_unsafe_condition,
#         "severity_high_potential_near_miss": severity_high_potential_near_miss,

#         "impact_on_people": impact_on_people,
#         "impact_on_asset": impact_on_asset,
#         "environmental_impact": environmental_impact,
#         "business_interruption": business_interruption,

#         "immediate_action_taken": immediate_action_taken,
#         "statutory_management_intimation": statutory_management_intimation,

#         "incident_description": incident_description,
#         "site_observations_evidence": site_observations_evidence,

#         "immediate_causes": immediate_causes,
#         "underlying_causes": underlying_causes,
#         "root_causes": root_causes,

#         "rca_tool_used": rca_tool_used,

#         "learning_recommendations": learning_recommendations,
#         "verification_closure": verification_closure,

#         "remarks_md": remarks_md,
#         "remarks_hse_head": remarks_hse_head,
#         "remarks_station_incharge": remarks_station_incharge,

#         "allotted_to_name": allotted_to_name,
#         "allotted_to_designation": allotted_to_designation,

#         "updated_by": updated_by,
#         "status":status,
#     }

#     # remove empty values
#     payload = {k: v for k, v in payload.items() if v is not None}

#     hiim = update_investigation(db, hiim_id, payload, annexure_files)

#     # =============================
#     # TRIGGER NOTIFICATION
#     # =============================
#     if status == "Investigation-Report-Filled":

#         await notify_investigation_report_filled(
#             db=db,
#             hiim=hiim,
#             background_tasks=background_tasks
#         )

#     return hiim
from fastapi import BackgroundTasks
from app.crud.hse.hse_major_notification import notify_investigation_report_filled


@router.put("/update/{hiim_id}")
async def update_hiim(
    hiim_id: int,

    report_number: str | None = Form(None),
    incident_date: str | None = Form(None),
    incident_time: str | None = Form(None),
    reporting_date: str | None = Form(None),

    location_details: str | None = Form(None),
    pipeline_name_section: str | None = Form(None),
    reported_by: str | None = Form(None),

    is_leak: bool | None = Form(None),
    is_spill: bool | None = Form(None),
    is_fire: bool | None = Form(None),
    is_explosion: bool | None = Form(None),
    is_injury: bool | None = Form(None),
    is_near_miss: bool | None = Form(None),
    is_other: bool | None = Form(None),

    severity_major: bool | None = Form(None),
    severity_minor: bool | None = Form(None),
    severity_near_miss: bool | None = Form(None),
    severity_unsafe_act: bool | None = Form(None),
    severity_unsafe_condition: bool | None = Form(None),
    severity_high_potential_near_miss: bool | None = Form(None),

    impact_on_people: str | None = Form(None),
    impact_on_asset: str | None = Form(None),
    environmental_impact: str | None = Form(None),
    business_interruption: str | None = Form(None),

    immediate_action_taken: str | None = Form(None),
    statutory_management_intimation: str | None = Form(None),

    incident_description: str | None = Form(None),
    site_observations_evidence: str | None = Form(None),

    immediate_causes: str | None = Form(None),
    underlying_causes: str | None = Form(None),
    root_causes: str | None = Form(None),

    rca_tool_used: str | None = Form(None),

    learning_recommendations: str | None = Form(None),
    verification_closure: str | None = Form(None),

    remarks_md: str | None = Form(None),
    remarks_hse_head: str | None = Form(None),
    remarks_station_incharge: str | None = Form(None),

    allotted_to_name: int | None = Form(None),
    allotted_to_designation: str | None = Form(None),

    updated_by: str | None = Form(None),
    status: str | None = Form(None),

    annexure_files: List[UploadFile] | None = File(None),

    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):

    payload = {
        "report_number": report_number,
        "incident_date": incident_date,
        "incident_time": incident_time,
        "reporting_date": reporting_date,

        "location_details": location_details,
        "pipeline_name_section": pipeline_name_section,
        "reported_by": reported_by,

        "is_leak": is_leak,
        "is_spill": is_spill,
        "is_fire": is_fire,
        "is_explosion": is_explosion,
        "is_injury": is_injury,
        "is_near_miss": is_near_miss,
        "is_other": is_other,

        "severity_major": severity_major,
        "severity_minor": severity_minor,
        "severity_near_miss": severity_near_miss,
        "severity_unsafe_act": severity_unsafe_act,
        "severity_unsafe_condition": severity_unsafe_condition,
        "severity_high_potential_near_miss": severity_high_potential_near_miss,

        "impact_on_people": impact_on_people,
        "impact_on_asset": impact_on_asset,
        "environmental_impact": environmental_impact,
        "business_interruption": business_interruption,

        "immediate_action_taken": immediate_action_taken,
        "statutory_management_intimation": statutory_management_intimation,

        "incident_description": incident_description,
        "site_observations_evidence": site_observations_evidence,

        "immediate_causes": immediate_causes,
        "underlying_causes": underlying_causes,
        "root_causes": root_causes,

        "rca_tool_used": rca_tool_used,

        "learning_recommendations": learning_recommendations,
        "verification_closure": verification_closure,

        "remarks_md": remarks_md,
        "remarks_hse_head": remarks_hse_head,
        "remarks_station_incharge": remarks_station_incharge,

        "allotted_to_name": allotted_to_name,
        "allotted_to_designation": allotted_to_designation,

        "updated_by": updated_by,
        "status": status,
    }

    payload = {k: v for k, v in payload.items() if v is not None}

    # =============================
    # UPDATE RECORD
    # =============================
    result = update_investigation(db, hiim_id, payload, annexure_files)

    # =============================
    # FETCH UPDATED OBJECT SAFELY
    # =============================
    hiim_obj = db.query(HSEIncidentInvestigationMaster).filter(
        HSEIncidentInvestigationMaster.hiim_id == hiim_id
    ).first()

    # =============================
    # TRIGGER NOTIFICATION
    # =============================
    if status == "Investigation-Report-Filled" and hiim_obj:

        await notify_investigation_report_filled(
            db=db,
            hiim=hiim_obj,
            background_tasks=background_tasks
        )
    hiim_obj = db.query(HSEIncidentInvestigationMaster).filter(
    HSEIncidentInvestigationMaster.hiim_id == hiim_id
    ).first()

    if status == "Inv-Engineer-Allotted" and hiim_obj:

        await notify_engineer_allotted(
            db=db,
            hiim=hiim_obj,
            background_tasks=background_tasks
        )
    return result


@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    return get_all_investigations(db)



@router.get("/investigations/{incident_id}/full")
def fetch_full_investigation(
    incident_id: int,
    db: Session = Depends(get_db)
):
    return get_full_investigation(db, incident_id)


@router.get("/investigation/{hiim_id}")
def get_investigation(
    hiim_id: int,
    db: Session = Depends(get_db)
):
  return get_investigation_by_id(db, hiim_id)