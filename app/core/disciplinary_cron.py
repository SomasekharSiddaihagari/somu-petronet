import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.database import SessionLocal
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
        
        
        
        
        