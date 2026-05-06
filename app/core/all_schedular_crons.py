from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from app.crud.leave.hr_leave_allocation_copy import run_monthly_leave_cron
from app.models.claim.out_of_pocket_claim import OutOfPocketClaim
IST = ZoneInfo("Asia/Kolkata")
scheduler = BackgroundScheduler(timezone=IST)
from sqlalchemy import func, text
from app.database import SessionLocal
from apscheduler.triggers.cron import CronTrigger
from app.models.claim.allowance_claim import AllowanceClaim
from app.models.claim.asset_claim_submission import AssetClaimSubmission
from app.models.claim.data_card_reimbursement import DataCardReimbursement
from app.models.claim.furniture_rm_reimbursement import FurnitureRMReimbursement
from app.models.claim.laptop_maintenance_reimbursement import LaptopMaintenanceReimbursement
from app.models.claim.leave_encashment import LeaveEncashment
from app.models.claim.mobile_bill_reimbursement import MobileBillReimbursement
from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement
from app.models.claim.vehicle_cm_reimbursement import VehicleCMReimbursement
from app.models.leave.hr_leave_application import HRLeaveApplication
from app.models.hr_action_tracker.disciplinary_incidents import DisciplinaryIncident



def auto_update_expired_suspensions():
    db: Session = SessionLocal()
    try:
        # Find all records where suspension has expired
        expired_records = (
            db.query(DisciplinaryIncident)
            .filter(DisciplinaryIncident.enable_suspension == True)
            .filter(DisciplinaryIncident.suspension_effective_to <= func.now())
            .all()
        )
        if not expired_records:
            return
 
        for record in expired_records:
            disciplinary_id = record.disciplinary_id
 
            # Change status to False
            record.enable_suspension = False
            db.add(record)
            db.commit()
 
            # ---- NOTIFICATION (Uncomment when needed) ----
            # asyncio.run(send_suspension_expiry_notification(db, disciplinary_id=disciplinary_id))
 
        print(f"[CRON] Updated: {len(expired_records)} records")
    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR]: {str(e)}")
    finally:
        db.close()

def auto_apply_hr_actions():
    db: Session = SessionLocal()
    try:
        # 1. Apply all past or present Transfers
        transfer_query = text("""
            UPDATE users
            SET station_id = subquery.new_station
            FROM (
                SELECT DISTINCT ON (user_id) user_id, new_station
                FROM employee_transfers
                WHERE DATE(effective_date) <= CURRENT_DATE AND is_deleted = FALSE
                ORDER BY user_id, effective_date DESC, id DESC
            ) AS subquery
            WHERE users.user_id = subquery.user_id 
            AND users.station_id IS DISTINCT FROM subquery.new_station;
        """)
        db.execute(transfer_query)

        # 2. Apply all past or present Promotions
        promotion_query = text("""
            UPDATE users
            SET grade = subquery.new_grade, designation = subquery.new_designation
            FROM (
                SELECT DISTINCT ON (user_id) user_id, new_grade, new_designation
                FROM promotions
                WHERE DATE(effective_date) <= CURRENT_DATE AND is_deleted = FALSE
                ORDER BY user_id, effective_date DESC, id DESC
            ) AS subquery
            WHERE users.user_id = subquery.user_id 
            AND (users.grade IS DISTINCT FROM subquery.new_grade OR users.designation IS DISTINCT FROM subquery.new_designation);
        """)
        db.execute(promotion_query)
        db.commit()
        print(f"[CRON] Successfully checked and applied pending HR Transfers & Promotions")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR auto_apply_hr_actions]: {str(e)}")
    finally:
        db.close()
        
def auto_withdraw_pending_leaves():
    """
    Automatically convert Pending leaves older than 7 days
    to 'Withdraw Approved'
    """

    db: Session = SessionLocal()

    try:
        seven_days_ago = func.now() - text("interval '7 days'")

        updated_count = (
            db.query(HRLeaveApplication)
            .filter(func.lower(HRLeaveApplication.status) == "pending")
            .filter(HRLeaveApplication.created_at <= seven_days_ago)
            .update(
                {
                    HRLeaveApplication.status: "Auto Rejected",
                    HRLeaveApplication.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        db.commit()

        print(f"[CRON] Auto-withdraw completed. Updated: {updated_count} records")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR] {str(e)}")

    finally:
        db.close()

def auto_lapse_asset_claims():
    """
    Automatically lapse asset claim submissions that have been
    sitting in an approval stage for more than 15 days
    """

    db: Session = SessionLocal()

    try:
        fifteen_days_ago = func.now() - text("interval '15 days'")

        # Stage 1: Supervisor hasn't acted in 15 days (timer = created_at)
        stage1_count = (
            db.query(AssetClaimSubmission)
            .filter(AssetClaimSubmission.status == "Pending Supervisor Approval")
            .filter(AssetClaimSubmission.created_at <= fifteen_days_ago)
            .update(
                {
                    AssetClaimSubmission.status: "Auto Lapsed",
                    AssetClaimSubmission.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 2: HR hasn't acted in 15 days (timer = updated_by_supervisor)
        stage2_count = (
            db.query(AssetClaimSubmission)
            .filter(AssetClaimSubmission.status == "Pending HR Approval")
            .filter(AssetClaimSubmission.updated_by_supervisor <= fifteen_days_ago)
            .update(
                {
                    AssetClaimSubmission.status: "Auto Lapsed",
                    AssetClaimSubmission.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 3: Finance hasn't acted in 15 days (timer = updated_by_hr)
        stage3_count = (
            db.query(AssetClaimSubmission)
            .filter(AssetClaimSubmission.status == "Pending Finance Approval")
            .filter(AssetClaimSubmission.updated_by_hr <= fifteen_days_ago)
            .update(
                {
                    AssetClaimSubmission.status: "Auto Lapsed",
                    AssetClaimSubmission.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        db.commit()

        total = stage1_count + stage2_count + stage3_count
        print(f"[CRON] Auto-lapse completed. Stage1: {stage1_count} | Stage2: {stage2_count} | Stage3: {stage3_count} | Total: {total} records")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR] Auto-lapse asset claims failed: {str(e)}")

    finally:
        db.close()

def auto_lapse_leave_encashment():
    """
    Automatically lapse leave encashment requests that have been
    sitting in an approval stage for more than 15 days
    """

    db: Session = SessionLocal()

    try:
        fifteen_days_ago = func.now() - text("interval '15 days'")

        # Stage 1: Supervisor hasn't acted in 15 days (timer = created_at)
        stage1_count = (
            db.query(LeaveEncashment)
            .filter(LeaveEncashment.status == "Pending Supervisor Approval")
            .filter(LeaveEncashment.created_at <= fifteen_days_ago)
            .update(
                {
                    LeaveEncashment.status: "Auto Lapsed",
                    LeaveEncashment.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 2: HR hasn't acted in 15 days (timer = updated_by_supervisor)
        stage2_count = (
            db.query(LeaveEncashment)
            .filter(LeaveEncashment.status == "Pending HR Approval")
            .filter(LeaveEncashment.updated_by_supervisor <= fifteen_days_ago)
            .update(
                {
                    LeaveEncashment.status: "Auto Lapsed",
                    LeaveEncashment.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 3: Finance hasn't acted in 15 days (timer = updated_by_hr)
        stage3_count = (
            db.query(LeaveEncashment)
            .filter(LeaveEncashment.status == "Pending Finance Approval")
            .filter(LeaveEncashment.updated_by_hr <= fifteen_days_ago)
            .update(
                {
                    LeaveEncashment.status: "Auto Lapsed",
                    LeaveEncashment.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        db.commit()

        total = stage1_count + stage2_count + stage3_count
        print(f"[CRON] Leave Encashment Auto-lapse completed. Stage1: {stage1_count} | Stage2: {stage2_count} | Stage3: {stage3_count} | Total: {total} records")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR] Leave Encashment Auto-lapse failed: {str(e)}")

    finally:
        db.close()

def auto_lapse_allowance_claim():
    """
    Automatically lapse allowance claims that have been
    sitting in an approval stage for more than 15 days
    """

    db: Session = SessionLocal()

    try:
        fifteen_days_ago = func.now() - text("interval '15 days'")

        # Stage 1: Supervisor hasn't acted in 15 days (timer = created_at)
        stage1_count = (
            db.query(AllowanceClaim)
            .filter(AllowanceClaim.status == "Pending Supervisor Approval")
            .filter(AllowanceClaim.created_at <= fifteen_days_ago)
            .update(
                {
                    AllowanceClaim.status: "Auto Lapsed",
                    AllowanceClaim.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 2: HR hasn't acted in 15 days (timer = updated_by_supervisor)
        stage2_count = (
            db.query(AllowanceClaim)
            .filter(AllowanceClaim.status == "Pending HR Approval")
            .filter(AllowanceClaim.updated_by_supervisor <= fifteen_days_ago)
            .update(
                {
                    AllowanceClaim.status: "Auto Lapsed",
                    AllowanceClaim.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 3: Finance hasn't acted in 15 days (timer = updated_by_hr)
        stage3_count = (
            db.query(AllowanceClaim)
            .filter(AllowanceClaim.status == "Pending Finance Approval")
            .filter(AllowanceClaim.updated_by_hr <= fifteen_days_ago)
            .update(
                {
                    AllowanceClaim.status: "Auto Lapsed",
                    AllowanceClaim.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        db.commit()

        total = stage1_count + stage2_count + stage3_count
        print(f"[CRON] Allowance Claim Auto-lapse completed. Stage1: {stage1_count} | Stage2: {stage2_count} | Stage3: {stage3_count} | Total: {total} records")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR] Allowance Claim Auto-lapse failed: {str(e)}")

    finally:
        db.close()

def auto_lapse_reimbursement(model):
    """
    Generic auto-lapse for any reimbursement model
    that has the same approval stage fields
    """
    db: Session = SessionLocal()

    try:
        fifteen_days_ago = func.now() - text("interval '15 days'")

        # Stage 1: Supervisor hasn't acted in 15 days (timer = created_at)
        stage1_count = (
            db.query(model)
            .filter(model.status == "Pending Supervisor Approval")
            .filter(model.created_at <= fifteen_days_ago)
            .update(
                {
                    model.status: "Auto Lapsed",
                    model.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 2: HR hasn't acted in 15 days (timer = updated_by_supervisor)
        stage2_count = (
            db.query(model)
            .filter(model.status == "Pending HR Approval")
            .filter(model.updated_by_supervisor <= fifteen_days_ago)
            .update(
                {
                    model.status: "Auto Lapsed",
                    model.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 3: Finance hasn't acted in 15 days (timer = updated_by_hr)
        stage3_count = (
            db.query(model)
            .filter(model.status == "Pending Finance Approval")
            .filter(model.updated_by_hr <= fifteen_days_ago)
            .update(
                {
                    model.status: "Auto Lapsed",
                    model.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        db.commit()

        total = stage1_count + stage2_count + stage3_count
        print(f"[CRON] {model.__tablename__} Auto-lapse completed. Stage1: {stage1_count} | Stage2: {stage2_count} | Stage3: {stage3_count} | Total: {total} records")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR] {model.__tablename__} Auto-lapse failed: {str(e)}")

    finally:
        db.close()

def auto_lapse_out_of_pocket_claim():
    """
    Automatically lapse out of pocket claims that have been
    sitting in an approval stage for more than 15 days
    """

    db: Session = SessionLocal()

    try:
        fifteen_days_ago = func.now() - text("interval '15 days'")

        # Stage 1: Supervisor hasn't acted in 15 days (timer = created_at)
        stage1_count = (
            db.query(OutOfPocketClaim)
            .filter(OutOfPocketClaim.status == "Pending Supervisor Approval")
            .filter(OutOfPocketClaim.created_at <= fifteen_days_ago)
            .update(
                {
                    OutOfPocketClaim.status: "Auto Lapsed",
                    OutOfPocketClaim.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 2: HOP hasn't acted in 15 days (timer = updated_by_supervisor)
        stage2_count = (
            db.query(OutOfPocketClaim)
            .filter(OutOfPocketClaim.status == "Pending HOP Approval")
            .filter(OutOfPocketClaim.updated_by_supervisor <= fifteen_days_ago)
            .update(
                {
                    OutOfPocketClaim.status: "Auto Lapsed",
                    OutOfPocketClaim.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        # Stage 3: Finance hasn't acted in 15 days (timer = updated_by_hop)
        stage3_count = (
            db.query(OutOfPocketClaim)
            .filter(OutOfPocketClaim.status == "Pending Finance Approval")
            .filter(OutOfPocketClaim.updated_by_hop <= fifteen_days_ago)
            .update(
                {
                    OutOfPocketClaim.status: "Auto Lapsed",
                    OutOfPocketClaim.updated_at: func.now()
                },
                synchronize_session=False
            )
        )

        db.commit()

        total = stage1_count + stage2_count + stage3_count
        print(f"[CRON] Out of Pocket Claim Auto-lapse completed. Stage1: {stage1_count} | Stage2: {stage2_count} | Stage3: {stage3_count} | Total: {total} records")

    except Exception as e:
        db.rollback()
        print(f"[CRON ERROR] Out of Pocket Claim Auto-lapse failed: {str(e)}")

    finally:
        db.close()







    
def auto_lapse_all_reimbursements():
    auto_lapse_reimbursement(DataCardReimbursement)
    auto_lapse_reimbursement(FurnitureRMReimbursement)
    auto_lapse_reimbursement(LaptopMaintenanceReimbursement)
    auto_lapse_reimbursement(MobileBillReimbursement)
    auto_lapse_reimbursement(VehicleCMReimbursement)







def start_auto_withdraw_scheduler():
    scheduler.add_job(
        func=auto_withdraw_pending_leaves,
        trigger=CronTrigger(hour=1, minute=0, timezone=IST),
        id="auto_withdraw_pending_leaves_daily",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    
    print("Auto Withdraw Pending Leave scheduler started (Daily 1:00 AM IST)")
    
    
    
def start_asset_claim_auto_lapse_scheduler():
    scheduler.add_job(
        func=auto_lapse_asset_claims,
        trigger=CronTrigger(hour=1, minute=0, timezone=IST),
        id="auto_lapse_asset_claims_daily",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    print("Asset Claim Auto-Lapse scheduler started (Daily 1:00 AM IST)")
    
    
    
def start_leave_encashment_auto_lapse_scheduler():
    scheduler.add_job(
        func=auto_lapse_leave_encashment,
        trigger=CronTrigger(hour=1, minute=0, timezone=IST),
        id="auto_lapse_leave_encashment_daily",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    print("Leave Encashment Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
    
def start_allowance_claim_auto_lapse_scheduler():
    scheduler.add_job(
        func=auto_lapse_allowance_claim,
        trigger=CronTrigger(hour=1, minute=0, timezone=IST),
        id="auto_lapse_allowance_claim_daily",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    print("Allowance Claim Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
    
def start_reimbursement_auto_lapse_scheduler():
    scheduler.add_job(
        func=auto_lapse_all_reimbursements,
        trigger=CronTrigger(hour=1, minute=0, timezone=IST),
        id="auto_lapse_all_reimbursements_daily",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    print("Reimbursement Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
def start_suspension_expiry_scheduler():
    scheduler.add_job(
        func=auto_update_expired_suspensions,
        trigger=CronTrigger(hour=2, minute=0, timezone=IST),  # Daily 2:00 AM IST
        id="auto_update_expired_suspensions_daily",
        replace_existing=True,
    )
    print("Disciplinary Suspension Expiry scheduler registered")
    
    
def start_hr_actions_scheduler():
    scheduler.add_job(
        func=auto_apply_hr_actions,
        trigger=CronTrigger(hour=1, minute=30, timezone=IST),  # Daily 1:30 AM IST
        id="auto_apply_hr_actions_daily",
        replace_existing=True,
    )
    print("HR Actions (Transfers & Promotions) scheduler registered")


def start_out_of_pocket_auto_lapse_scheduler():
    scheduler.add_job(
        func=auto_lapse_out_of_pocket_claim,
        trigger=CronTrigger(hour=1, minute=0, timezone=IST),
        id="auto_lapse_out_of_pocket_claim_daily",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    print("Out of Pocket Claim Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
    
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


# def start_leave_encashment_auto_lapse_scheduler():
#     scheduler.add_job(
#         func=auto_lapse_leave_encashment,
#         trigger=CronTrigger(hour=1, minute=0, timezone=IST),
#         id="auto_lapse_leave_encashment_daily",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )
#     print("Leave Encashment Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
    
# def start_allowance_claim_auto_lapse_scheduler():
#     scheduler.add_job(
#         func=auto_lapse_allowance_claim,
#         trigger=CronTrigger(hour=1, minute=0, timezone=IST),
#         id="auto_lapse_allowance_claim_daily",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )
#     print("Allowance Claim Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
    
# def start_reimbursement_auto_lapse_scheduler():
#     scheduler.add_job(
#         func=auto_lapse_all_reimbursements,
#         trigger=CronTrigger(hour=1, minute=0, timezone=IST),
#         id="auto_lapse_all_reimbursements_daily",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )
#     print("Reimbursement Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
    
    
# def start_suspension_expiry_scheduler():
#     scheduler.add_job(
#         func=auto_update_expired_suspensions,
#         trigger=CronTrigger(hour=2, minute=0, timezone=IST),  # Daily 2:00 AM IST
#         id="auto_update_expired_suspensions_daily",
#         replace_existing=True,
#     )
#     print("Disciplinary Suspension Expiry scheduler registered")
    
    
# def start_hr_actions_scheduler():
#     scheduler.add_job(
#         func=auto_apply_hr_actions,
#         trigger=CronTrigger(hour=1, minute=30, timezone=IST),  # Daily 1:30 AM IST
#         id="auto_apply_hr_actions_daily",
#         replace_existing=True,
#     )
#     print("HR Actions (Transfers & Promotions) scheduler registered")


# def start_out_of_pocket_auto_lapse_scheduler():
#     scheduler.add_job(
#         func=auto_lapse_out_of_pocket_claim,
#         trigger=CronTrigger(hour=1, minute=0, timezone=IST),
#         id="auto_lapse_out_of_pocket_claim_daily",
#         replace_existing=True,
#         max_instances=1,
#         coalesce=True,
#     )
#     print("Out of Pocket Claim Auto-Lapse scheduler registered (Daily 1:00 AM IST)")
 