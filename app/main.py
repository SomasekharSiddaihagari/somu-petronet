# app/main.py
import os
from fastapi import FastAPI
from sqlalchemy import text
# from app.crud.leave.hr_leave_crud import allocate_smart_leaves
# from app.crud.leave.analytics_crud import allocate_smart_leaves
from app.core.all_schedular_crons import auto_apply_hr_actions, start_allowance_claim_auto_lapse_scheduler, start_asset_claim_auto_lapse_scheduler, start_auto_withdraw_scheduler, start_hr_actions_scheduler, start_leave_encashment_auto_lapse_scheduler, start_out_of_pocket_auto_lapse_scheduler, start_reimbursement_auto_lapse_scheduler, start_suspension_expiry_scheduler
from app.crud.leave.hr_leave_allocation import run_monthly_leave_cron
from app.middlewares.jwt_middleware import JWTMiddleware
from app.routers.circular_management import circular_user_activity_router
from app.routers.permit_management.composit_permit import composite_electrical_energization_permit, composite_electrical_isolation_permit, composite_toolbox_talk, composite_toolbox_talk_participant, composite_work_permit
from app.routers.permit_management.work_height_permit import work_at_height_electrical_energization_permit, work_at_height_electrical_isolation_permit, work_at_height_permit, work_at_height_toolbox_talk, work_at_height_toolbox_talk_participant
from app.database import SessionLocal, engine, Base
from app.routers import ResetPasswordRouter, UserAuth, UserAuthR2, secured, superviser  # import routers
from app.models import UserModel as UserModel # noqa: F401, ensures models are registered
from app.routers import  MenuRouter, SubMenuRouter, RolePermissionRouter
from app.models.MOC.StationModel import Station
from fastapi.middleware.cors import CORSMiddleware
from app.models.MOC.MocRequestModel import MoCRequest
from app.routers.MOC import MOCRouter, HIRARouter,MoCCloserRouter
from app.routers.MOC import StationRouter
from app.routers import RoleRouter, NotificationRouter
from app.routers.MOC import MoCfile
from app.routers.claim import allowance_claim_router, asset_api_validation, claim_get_api_router,asset_claim_router,encashment_router,mobile_bill_reimbursement_router, ra_claim_router,furniture_items_router,allowance_claim_router,get_all_asset_claim_card_detials_router,fuel_rate_config_router
from app.routers.leave.hr_comp_off_router import router as comp_off_router
from app.routers.digital_logbook.digital_cp_reading import cp_reading_dkn_entry_router, cp_reading_dkn_master_router, cp_reading_hsn_entry_router, cp_reading_hsn_master_router, cp_reading_mlr_entry_router, cp_reading_mlr_master_router, cp_reading_ner_entry_router, cp_reading_ner_master_router
from app.routers.digital_logbook.digital_cp_reading.cp_reading_master_router import router as cp_reading_master_router
from app.routers.digital_logbook.digital_cp_reading.cp_reading_entry_router import router as cp_reading_entry_router
from app.routers.digital_logbook.digital_daily_safety import daily_safty_checklist_router
from app.routers.digital_logbook.digital_daily_sampling import daily_sampling_entry_router, daily_sampling_master_router
from app.routers.digital_logbook.digital_kptcl import kptcl_dkn_entry_router, kptcl_dkn_master_router, kptcl_hsn_entry_router, kptcl_hsn_master_router, kptcl_ner_entry_router, kptcl_ner_master_router
from app.routers.digital_logbook.digital_logbook_dkn import dkn_digital_logbook_entry_router, dkn_digital_logbook_router
from app.routers.digital_logbook.digital_logbook_hsn import hsn_digital_logbook_entry_router, hsn_digital_logbook_router
from app.routers.digital_logbook.digital_logbook_linewalker import line_walker_entry_router, line_walker_master_router, supervisor_entry_router
from app.routers.digital_logbook.digital_logbook_main import logbook_shift_master_router
from app.routers.digital_logbook.digital_logbook_mlr import mlr_digital_logbook_entry_router, mlr_digital_logbook_router
# from app.core.scheduler import start_scheduler, shutdown_scheduler
from app.routers.digital_logbook.digital_logbook_ner import ner_digital_logbook_entry_router, ner_digital_logbook_router

from app.routers.digital_logbook.digital_logbook_security_guard import security_guard_report_router
from app.routers.digital_logbook.digital_logbook_security_guard import security_guard_report_line
from app.routers.digital_logbook.digital_mfm_logbook import mfm_log_entry_dsk_router, mfm_log_hsn2_entry_router_router, mfm_log_hsn2_master_router_router, mfm_log_hsn_entry_router, mfm_log_hsn_master_router, mfm_log_master_dsk_router, mfm_log_mlr_entry_router, mfm_log_mlr_master_router, mfm_log_mlr_two_entry_router, mfm_log_mlr_two_master_router, mfm_log_ner_entry_router, mfm_log_ner_master_router, mfm_log_ner_page2_master_router, mfm_plt_detail_dsk_router
from app.routers.digital_logbook.digital_npt import npt_report_entry_router, npt_report_master_router
from app.routers.digital_logbook.digital_pressure import pressure_log_entry_router, pressure_log_master_router
from app.routers.digital_logbook.digital_shift_handover import shift_handover_master_router, shift_handover_task_router
from app.routers.digital_logbook.digital_shift_takeover import shift_takeover_router
from app.routers.digital_logbook.digital_tank_dip import tank_dip_memo_router
from app.routers.digital_logbook.digital_vibration import vibration_temperature_entry_mlr_router, vibration_temperature_entry_ner_router, vibration_temperature_master_mlr_router, vibration_temperature_master_ner_router
from app.routers.digital_logbook.geo_fencing import access_control_router, access_router, approval_router, protected_router, shift_router, shift_task_router, token_verification
from app.routers.gate_pass import igGatePassRouter,materialGatePassRouter,ogGatePassRouter, otherGatePassRouter,rgGatePassRouter
from app.routers.employees_info import asset_declaration_routers, declaration_settings,employee_family_routers,employee_form_12c_routers, user_finance_routers,all_in_router_emoloyee_info,user_education
from app.routers.leave import emoloyee_weekof,analytics_route, hr_leave_router, leave_comp_of, leave_master_table, leave_number_days, leave_type, public_holiday,leave_report

from app.routers.permit_management.dashboard import dashboard
from app.routers.travel_expense import travel_forms_router, travel_meal_allowance,travel_daily_router,travel_validation_router
from app.routers.travel_expense import travel_requisition_router,travel_travel_router,travel_hotel_router,travel_car_router,travel_daily_router,travel_expense_detail_router,travel_expense_sheet_router
from app.routers.employees_info.user_vehicle_router import router as UserVehicleRouter
from app.routers.claim.data_card_reimbursement_router import router as data_card_reimbursement_router
from app.routers.claim.furniture_rm_reimbursement_router import router as furniture_rm_router
from app.routers.claim.vehicle_cm_reimbursement_router import router as vehicle_cm_router
from app.routers.claim.laptop_maintenance_reimbursement_router import (
    router as laptop_maintenance_router
)
from app.routers.claim.out_of_pocket_claim_router import (
    router as out_of_pocket_router
)
from app.routers.gate_pass.sap_po_api import router as sap_po_router
from app.routers.claim import validation_router
from app.routers.travel_expense.travel_meal_da_validation import router as allowance_router


from app.routers.digital_logbook.digital_fire.fire_engine_test_master_router import router as fire_engine_test_master_router
from app.routers.digital_logbook.digital_10K_tank.tank_10kl_ffe_master_router import router as tank_10kl_ffe_master_router
from app.routers.digital_logbook.digital_10K_tank.tank_10kl_ffe_entry_router import router as tank_10kl_ffe_entry_router
from app.routers.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_router import router as product_dispatch_category_router
from app.routers.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_hourly_log_router import router as product_dispatch_hourly_log_router
from app.routers.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_log_router import router as product_dispatch_shift_log_router
from app.routers.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shutdown_log_router import router as product_dispatch_shutdown_log_router
from app.routers.digital_logbook.digital_mfm_accounting.mfm_accounting_hsn_router import router as mfm_accounting_hsn_router
from app.routers.digital_logbook.digital_mfm_accounting.mfm_accounting_dkn_router import router as mfm_accounting_dkn_router
from app.routers.digital_logbook.digital_mfm_logbook.mfm_shutdown_detail_dsk_router import router as mfm_shutdown_detail_dsk_router   
from app.routers.permit_management import composite_electrical_energization_router,composite_electrical_isolation_router,composite_toolbox_talk_participant_router,composite_toolbox_talk_router,cwp_router_master,wah_electrical_energization_router,wah_toolbox_participant_router,wah_electrical_isolation_router,wah_toolbox_talk_router,work_at_height_router

from app.routers.hse.incident_report_router import (
    router as incident_report_router
)
from app.routers.hse.incident_impact_assessment_router import (
    router as incident_impact_router
)
from app.routers.hse.incident_cause_analysis_router import (
    router as incident_cause_router
)
from app.routers.hse.incident_prevention_router import (
    router as incident_prevention_router
)
from app.routers.hse.incident_investigation_team_router import (
    router as incident_investigation_team_router
)
from app.routers.hse.hse_incident_investigation_router import (router as investigation_master_router
)

from app.routers.hse.hse_incident_investigation_team_router import (
    router as investigation_master_team_router
)

from app.routers.hse.hse_incident_rca_5why_router import (
    router as rca_5why_router
)

from app.routers.hse.fta_top_event_router import (
    router as fta_top_event_router
)
from app.routers.hse.fta_intermediate_event_router import (
    router as fta_intermediate_event_router
)
from app.routers.hse.fta_basic_event_router import (
    router as fta_basic_event_router
)
from app.routers.hse.hse_incident_capa_actions_router import (
    router as incident_capa_actions_router
)

from app.routers.hse.capa_report_router import (
    router as capa_report_router
)

from app.routers.hse.capa_document_change_router import (
    router as capa_document_change_router
)

from app.routers.hse.safety_committee_router import (
    router as safety_committee_router
)
from app.routers.hse.safety_committee_meeting_router import (
    router as safety_committee_meeting_router
)
from app.routers.hse.safety_committee_minutes_router import (
    router as safety_committee_minutes_router
)
from app.routers.hse.safety_committee_minutes_discussion_child_router import (
    router as safety_committee_minutes_discussion_child_router
)
from app.routers.hse.safety_committee_minutes_members_router import (
    router as safety_committee_minutes_members_router
)
from app.routers.hse.safety_committee_minutes_incidents_router import (
    router as safety_committee_minutes_incidents_router
)
from app.routers.employees_info.employee_bank_router import router as bank_router 
from app.routers.leave.hr_comp_off_router import router as comp_off_router,validate_comp_off_leave
from app.routers.employees_info.family_submission_router import router as family_submission_router

from app.routers.circular_management.publisher_master_router import (router as publisher_master_router)
from app.routers.circular_management.circular_master_router import(router as circular_master_router)
from app.routers.digital_logbook.digital_erv_logbook import erv_vehicle_inspection_entry_router,erv_logbook_master_router
from app.routers.circular_management.category_master_router import(router as category_master_router)
from app.routers.circular_management.sub_category_master_router import router as sub_category_master_router
from app.routers.circular_management.group_master_router import router as group_master_router
from app.routers.circular_management.circular_user_activity_router import router as circular_user_activity_route
from app.routers.digital_logbook.digital_dg_250kva.dg_250kva_master_router import router as dg_250kva_master_router
from app.routers.digital_logbook.digital_dg_250kva.dg_250kva_entry_router import router as dg_250kva_entry_router
from app.routers.digital_logbook.digital_fire import fire_engine_test_entry_router
from app.routers.hr_action_tracker.action_master_router import router as action_master_router
from app.routers.hr_action_tracker.disciplinary_master_router import router as disciplinary_master_router
from app.routers.hr_action_tracker.emp_transfer_master_router import router as emp_transfer_master_router
from app.routers.hr_action_tracker.performance_master_router import router as performance_master_router
from app.routers.hr_action_tracker.promotion_master_router import router as promotion_master_router
from app.routers.upload_router import upload_router


# After the last HSE include_router, add:

from app.routers.permit_management.jsa_router import router as jsa_router
from app.routers.permit_management.jsa_steps_router import router as jsa_steps_router



from fastapi.openapi.utils import get_openapi
from app.middlewares.jwt_middleware import JWTMiddleware




from app.routers import file_router



from fastapi.staticfiles import StaticFiles
app = FastAPI(
    title="Petronet"
)


# Create tables (for dev only; in production, use Alembic migrations)
Base.metadata.create_all(bind=engine)

app.mount("/files", StaticFiles(directory="files"), name="files")
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



origins = [
    "*",  # allow all (for now, can restrict later)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow all methods including OPTIONS
    allow_headers=["*"],   # allow all headers
)

# @app.on_event("startup")
# def startup_event():
#     start_scheduler()

# @app.on_event("shutdown")
# def shutdown_event():
#     shutdown_scheduler()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Petronet API",
        version="1.0",
        description="Petronet Backend API",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# app.add_middleware(JWTMiddleware)
# Include routers
app.include_router(UserAuth.router)
app.include_router(file_router.router)
app.include_router(MenuRouter.router)
app.include_router(SubMenuRouter.router)
app.include_router(RolePermissionRouter.router)
app.include_router(MOCRouter.router)
app.include_router(StationRouter.router)
app.include_router(RoleRouter.router)
app.include_router(HIRARouter.router)
app.include_router(MoCfile.router)
app.include_router(NotificationRouter.router)
app.include_router(MoCCloserRouter.router)
app.include_router(igGatePassRouter.router)
app.include_router(materialGatePassRouter.router)
app.include_router(ogGatePassRouter.router)
app.include_router(rgGatePassRouter.router)
app.include_router(otherGatePassRouter.router)
app.include_router(ResetPasswordRouter.router)
app.include_router(asset_declaration_routers.router)
app.include_router(employee_family_routers.router)
app.include_router(bank_router)
app.include_router(employee_form_12c_routers.router)
app.include_router(UserAuthR2.router)
app.include_router(user_finance_routers.router)
app.include_router(all_in_router_emoloyee_info.router)
app.include_router(declaration_settings.router)
app.include_router(user_education.router)
app.include_router(superviser.router)
app.include_router(leave_type.router)
app.include_router(leave_comp_of.router)
app.include_router(leave_master_table.router)
app.include_router(leave_number_days.router)
app.include_router(analytics_route.router)
app.include_router(hr_leave_router.router)
app.include_router(leave_report.router)
app.include_router(public_holiday.router)
app.include_router(travel_forms_router.router)
app.include_router(travel_meal_allowance.router)
app.include_router(travel_requisition_router.router)
app.include_router(travel_travel_router.router)
app.include_router(travel_hotel_router.router)
app.include_router(travel_car_router.router)
# app.include_router(travel_daily_router.router)
app.include_router(travel_validation_router.router)
app.include_router(travel_daily_router.router)
app.include_router(travel_expense_sheet_router.router)
app.include_router(travel_expense_detail_router.router)
app.include_router(UserVehicleRouter)
# app.include_router(secured.router)
app.include_router(claim_get_api_router.router)
app.include_router(asset_claim_router.router)
app.include_router(encashment_router.router)  
app.include_router(mobile_bill_reimbursement_router.router)
app.include_router(ra_claim_router.router)
app.include_router(asset_api_validation.router)
app.include_router(validation_router.router)
app.include_router(fuel_rate_config_router.router)


app.include_router(data_card_reimbursement_router)
app.include_router(furniture_rm_router)
app.include_router(vehicle_cm_router)
app.include_router(laptop_maintenance_router)
app.include_router(out_of_pocket_router)
app.include_router(allowance_claim_router.router)
app.include_router(furniture_items_router.router)
app.include_router(allowance_router)
app.include_router(emoloyee_weekof.router)
app.include_router(get_all_asset_claim_card_detials_router.router)
app.include_router(sap_po_router)
app.include_router(logbook_shift_master_router.router)

app.include_router(daily_safty_checklist_router.router)

app.include_router(dkn_digital_logbook_entry_router.router)
app.include_router(dkn_digital_logbook_router.router)
app.include_router(hsn_digital_logbook_entry_router.router)
app.include_router(hsn_digital_logbook_router.router)
app.include_router(mlr_digital_logbook_entry_router.router)
app.include_router(mlr_digital_logbook_router.router)
app.include_router(ner_digital_logbook_entry_router.router)
app.include_router(ner_digital_logbook_router.router)

app.include_router(line_walker_entry_router.router)
app.include_router(line_walker_master_router.router)
app.include_router(supervisor_entry_router.router)

# app.include_router(access_router.router)
app.include_router(approval_router.router)
app.include_router(protected_router.router)
app.include_router(shift_router.router)
app.include_router(shift_handover_task_router.router)  

app.include_router(access_control_router.router)
app.include_router(token_verification.router)
app.include_router(erv_logbook_master_router.router)
app.include_router(erv_vehicle_inspection_entry_router.router)
# digital book routes

app.include_router(fire_engine_test_master_router)
app.include_router(fire_engine_test_entry_router.router)
app.include_router(tank_10kl_ffe_master_router)
app.include_router(tank_10kl_ffe_entry_router)
app.include_router(product_dispatch_category_router)
app.include_router(product_dispatch_hourly_log_router)
app.include_router(product_dispatch_shift_log_router)
app.include_router(product_dispatch_shutdown_log_router)
app.include_router(mfm_accounting_hsn_router)
app.include_router(mfm_accounting_dkn_router)
app.include_router(mfm_shutdown_detail_dsk_router)  

app.include_router(comp_off_router)



app.include_router(cp_reading_dkn_entry_router.router)  
app.include_router(cp_reading_dkn_master_router.router) 
app.include_router(cp_reading_hsn_entry_router.router)  
app.include_router(cp_reading_hsn_master_router.router)  
app.include_router(cp_reading_mlr_entry_router.router)  
app.include_router(cp_reading_mlr_master_router.router)  
app.include_router(cp_reading_ner_entry_router.router)  
app.include_router(cp_reading_ner_master_router.router)  
app.include_router(cp_reading_master_router)
app.include_router(cp_reading_entry_router)

app.include_router(daily_sampling_entry_router.router)  
app.include_router(daily_sampling_master_router.router)  
app.include_router(kptcl_dkn_entry_router.router)  
app.include_router(kptcl_dkn_master_router.router)  
app.include_router(kptcl_hsn_entry_router.router)  
app.include_router(kptcl_hsn_master_router.router)  
app.include_router(kptcl_ner_entry_router.router)  
app.include_router(kptcl_ner_master_router.router)  
app.include_router(security_guard_report_router.router)  
app.include_router(security_guard_report_line.router)  
app.include_router(mfm_log_entry_dsk_router.router)  
app.include_router(mfm_log_hsn_entry_router.router)  
app.include_router(mfm_log_hsn_master_router.router)  
app.include_router(mfm_log_hsn2_entry_router_router.router)  
app.include_router(mfm_log_hsn2_master_router_router.router)  
app.include_router(mfm_log_master_dsk_router.router)  
app.include_router(mfm_log_mlr_entry_router.router)  
app.include_router(mfm_log_mlr_master_router.router)  
app.include_router(mfm_log_mlr_two_entry_router.router)  
app.include_router(mfm_log_mlr_two_master_router.router)  
app.include_router(mfm_log_ner_entry_router.router)  
app.include_router(mfm_log_ner_master_router.router)  
app.include_router(mfm_log_ner_page2_master_router.router)  
app.include_router(mfm_plt_detail_dsk_router.router)  
app.include_router(npt_report_entry_router.router)  
app.include_router(npt_report_master_router.router)  
app.include_router(pressure_log_entry_router.router)  
app.include_router(pressure_log_master_router.router)  
# app.include_router(shift_handover_master_router.router)  
# app.include_router(shift_takeover_router.router)  
app.include_router(tank_dip_memo_router.router)  
app.include_router(vibration_temperature_entry_mlr_router.router)  
app.include_router(vibration_temperature_entry_ner_router.router)  
app.include_router(vibration_temperature_master_mlr_router.router)  
app.include_router(vibration_temperature_master_ner_router.router)  


app.include_router(composite_electrical_energization_router.router)
app.include_router(composite_electrical_isolation_router.router)
app.include_router(composite_toolbox_talk_participant_router.router)
app.include_router(composite_toolbox_talk_router.router)
app.include_router(cwp_router_master.router)
app.include_router(wah_electrical_energization_router.router)
app.include_router(wah_electrical_isolation_router.router)
app.include_router(wah_toolbox_participant_router.router)
app.include_router(wah_toolbox_talk_router.router)
app.include_router(work_at_height_router.router)
app.include_router(shift_task_router.router)

# app.include_router(security_guard_report_router)
app.include_router(composite_work_permit.router)
app.include_router(composite_toolbox_talk.router)
app.include_router(composite_toolbox_talk_participant.router)
app.include_router(composite_electrical_isolation_permit.router)
app.include_router(composite_electrical_energization_permit.router)
app.include_router(work_at_height_toolbox_talk.router)
app.include_router(work_at_height_toolbox_talk_participant.router)
app.include_router(work_at_height_permit.router)
app.include_router(work_at_height_electrical_isolation_permit.router)
app.include_router(work_at_height_electrical_energization_permit.router)
app.include_router(dashboard.router)

# HSE

app.include_router(incident_report_router)
app.include_router(incident_impact_router)
app.include_router(incident_cause_router)
app.include_router(incident_prevention_router)
app.include_router(incident_investigation_team_router)
app.include_router(investigation_master_router)
app.include_router(investigation_master_team_router)
app.include_router(rca_5why_router)
app.include_router(fta_top_event_router)
app.include_router(fta_intermediate_event_router)
app.include_router(fta_basic_event_router)
app.include_router(incident_capa_actions_router)
app.include_router(capa_report_router)
app.include_router(capa_document_change_router)
app.include_router(safety_committee_minutes_incidents_router)

app.include_router(safety_committee_router)
app.include_router(safety_committee_meeting_router)
app.include_router(safety_committee_minutes_router)
app.include_router(safety_committee_minutes_members_router)
 
app.include_router(family_submission_router)


app.include_router(publisher_master_router)
app.include_router(circular_master_router)
app.include_router(category_master_router)
app.include_router(sub_category_master_router)
app.include_router(group_master_router)
app.include_router(circular_user_activity_route)

app.include_router(dg_250kva_master_router)
app.include_router(dg_250kva_entry_router)
app.include_router(action_master_router)
app.include_router(disciplinary_master_router)
app.include_router(emp_transfer_master_router)
app.include_router(performance_master_router)
app.include_router(promotion_master_router)

app.include_router(safety_committee_minutes_discussion_child_router)
app.include_router(upload_router)

app.include_router(jsa_router)
app.include_router(jsa_steps_router)

# -------------------------------------------------
# -------------------------------------------------
# APSCHEDULER SETUP
# - PRODUCTION: 1st of every month (IST)
# - TESTING: every 5 minutes (IST)
# -------------------------------------------------

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo
from app.database import SessionLocal
from apscheduler.triggers.cron import CronTrigger
IST = ZoneInfo("Asia/Kolkata")
scheduler = BackgroundScheduler(timezone=IST)
 
from apscheduler.triggers.interval import IntervalTrigger

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/healthz")
def health_check():
    try:
        # 🔍 Check DB connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "down",
            "reason": str(e)
        }
  
# -------- ALL CRONS RUN'S IN PRODUCTION MODE (EVERY NIGHT 1:00 AM IST) --------

def leave_cron_job():
    db = SessionLocal()
    try:
        run_monthly_leave_cron(db)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.on_event("startup")
def start_cron_jobs():
    leave_cron_job()
    auto_apply_hr_actions()
    start_auto_withdraw_scheduler()
    start_suspension_expiry_scheduler()
    start_hr_actions_scheduler()
    start_asset_claim_auto_lapse_scheduler()
    start_leave_encashment_auto_lapse_scheduler()
    start_allowance_claim_auto_lapse_scheduler()
    start_reimbursement_auto_lapse_scheduler()
    start_out_of_pocket_auto_lapse_scheduler()   

    scheduler.start()
    print("All HR Action Cron Jobs Initialized and Started")

@app.on_event("shutdown")
def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler shut down cleanly")


@app.on_event("startup")
def startup_event():
    shift_router.start_scheduler()


# -------- TEST MODE (EVERY 30 SECONDS) --------

# def leave_cron_job():
#     db = SessionLocal()
#     try:
#         run_monthly_leave_cron(db)
#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()

# def start_leave_scheduler_test():
#     scheduler.add_job(
#         func=leave_cron_job,
#         trigger=CronTrigger(minute="*/30", timezone=IST),
#         id="leave_allocation_test_every_5_min",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )

    
#     print("Leave allocation scheduler started (TEST MODE: every 30 Seconds, IST)")

# def start_asset_claim_auto_lapse_scheduler():
#     scheduler.add_job(
#         func=auto_lapse_asset_claims,
#         trigger=CronTrigger(second="*/30", timezone=IST),
#         id="auto_lapse_asset_claims_daily",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )

    
#     print("Asset Claim Auto-Lapse scheduler started (Every 30 Seconds, IST)")

# def start_auto_withdraw_scheduler_test_30sec():
#     scheduler.add_job(
#         func=auto_withdraw_pending_leaves,
#         trigger=CronTrigger(second="*/30", timezone=IST),
#         id="auto_withdraw_pending_leaves_test_30sec",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )

   
#     print("Auto Withdraw scheduler started (TEST MODE: every 30 seconds IST)")

# @app.on_event("startup")
# def start_auto_withdraw_cron():
#     start_auto_withdraw_scheduler_test_30sec()
#     start_asset_claim_auto_lapse_scheduler() 
   
#     scheduler.start()
#     print("🔥 Auto Withdraw Cron Initialized")

# @app.on_event("shutdown")
# def shutdown_scheduler():
#     if scheduler.running:
#         scheduler.shutdown(wait=False)
#         print("Scheduler shut down cleanly")

