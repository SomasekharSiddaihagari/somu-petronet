from app.database import SessionLocal
from app.crud.leave.hr_leave_allocation import run_monthly_leave_cron

db = SessionLocal()

try:
    run_monthly_leave_cron(db)
finally:
    db.close()
