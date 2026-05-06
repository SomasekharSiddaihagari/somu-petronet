from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime, date
from app.schemas.claim.asset_claim_schema import (
    AssetClaimCreate,
    AssetClaimUpdate
)
 
# -------------------------------------------------
# Generate Asset Claim Reference ID
# Format: AC/2025/000001
# -------------------------------------------------
def generate_asset_claim_ref(db: Session) -> str:
    year = datetime.now().year
    prefix = f"AC/{year}/"
 
    query = text("""
        SELECT claim_ref_id
        FROM asset_claim
        WHERE claim_ref_id LIKE :prefix
        ORDER BY asset_claim_id DESC
        LIMIT 1
    """)
 
    last = db.execute(query, {"prefix": f"{prefix}%"}).fetchone()
 
    next_no = 1
    if last and last[0]:
        next_no = int(last[0].split("/")[-1]) + 1
 
    return f"{prefix}{str(next_no).zfill(6)}"
 
 
from dateutil.relativedelta import relativedelta
 
def calculate_buyback_date(
    claim_date: date,
    category: str,
    sub_category: str
) -> date | None:
 
    rules = {
        ("Laptop / Desktop", "Laptop / Desktop"): 3,
        ("Furniture", "Electronics"): 4,
        ("Furniture", "Utility & Decorative Furniture"): 6,
        ("Furniture", "Soft Furnishing"): 4,
        ("Furniture", "Sports Equipment"): 6,
    }
 
    years = rules.get((category, sub_category))
 
    if not years:
        return None  # buy back not applicable
 
    return claim_date + relativedelta(years=years)
 
# -------------------------------------------------
# CREATE ASSET CLAIM (INSERT + HISTORY)
# -------------------------------------------------
def create_asset_claim(db: Session, data: AssetClaimCreate):
    claim_ref_id = generate_asset_claim_ref(db)
 
    payload = data.model_dump()
    payload["claim_ref_id"] = claim_ref_id
 
    # 🔥 Calculate buy back date
    payload["buy_back_date"] = calculate_buyback_date(
        claim_date=payload["claim_date"],
        category=payload["category"],
        sub_category=payload["sub_category"],
    )
 
    query = text("""
        INSERT INTO asset_claim (
            claim_ref_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,
            claim_module,
            category,
            sub_category,
            claim_date,
            bought_back,
            buy_back_date,
            item_type,
            total_entitlement_limit,
            amount_utilized,
            balance_available,
            status,
            remarks,
            created_by
        )
        VALUES (
            :claim_ref_id,
            :employee_name,
            :employee_id,
            :department,
            :designation,
            :station,
            :grade,
            :claim_module,
            :category,
            :sub_category,
            :claim_date,
            :bought_back,
            :buy_back_date,
            :item_type,
            :total_entitlement_limit,
            :amount_utilized,
            :balance_available,
            :status,
            :remarks,
            :created_by
        )
        RETURNING asset_claim_id
    """)
 
    result = db.execute(query, payload)
    asset_claim_id = result.scalar()
 
    insert_asset_claim_history(db, asset_claim_id)
 
    db.commit()
 
    return {
        "asset_claim_id": asset_claim_id,
        "claim_ref_id": claim_ref_id
    }
 
 
 
# -------------------------------------------------
# UPDATE ASSET CLAIM (ROLE BASED + HISTORY)
# -------------------------------------------------
# -------------------------------------------------
# UPDATE ASSET CLAIM (SIMPLE UPDATE + HISTORY)
# -------------------------------------------------
def update_asset_claim(
    db: Session,
    asset_claim_id: int,
    data: AssetClaimUpdate
):
    payload = data.model_dump(exclude_unset=True)
 
    if not payload:
        return False
 
    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
 
    query = text(f"""
        UPDATE asset_claim
        SET {set_clause},
            updated_at = NOW()
        WHERE asset_claim_id = :asset_claim_id
    """)
 
    payload["asset_claim_id"] = asset_claim_id
    db.execute(query, payload)
 
    insert_asset_claim_history(db, asset_claim_id)
 
    db.commit()
    return True
 
 
# -------------------------------------------------
# INSERT HISTORY SNAPSHOT
# -------------------------------------------------
def insert_asset_claim_history(db: Session, asset_claim_id: int):
    history_sql = text("""
        INSERT INTO asset_claim_history (
            asset_claim_id,
            claim_ref_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,
            claim_module,
            category,
            sub_category,
            claim_date,
            bought_back,
            buy_back_submitted_date,
            bought_back_date,
            buy_back_date,
            item_type,
            total_entitlement_limit,
            amount_utilized,
            balance_available,
            status,
            remarks,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            updated_at
        )
        SELECT
            asset_claim_id,
            claim_ref_id,
            employee_name,
            employee_id,
            department,
            designation,
            station,
            grade,
            claim_module,
            category,
            sub_category,
            claim_date,
            bought_back,
            buy_back_date,
            buy_back_submitted_date,
            bought_back_date,  
            item_type,
            total_entitlement_limit,
            amount_utilized,
            balance_available,
            status,
            remarks,
            created_by,
            updated_by,
            updated_by_supervisor,
            updated_by_supervisor_name,
            updated_by_hr,
            updated_by_hr_name,
            updated_by_finance,
            updated_by_finance_name,
            NOW()
        FROM asset_claim
        WHERE asset_claim_id = :asset_claim_id
    """)
 
    db.execute(history_sql, {"asset_claim_id": asset_claim_id})
 
 