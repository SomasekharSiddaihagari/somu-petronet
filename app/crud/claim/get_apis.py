from sqlalchemy.orm import Session
from sqlalchemy import text

def get_asset_claims_by_user_id_sql(db: Session, user_id: str):
    sql = text("""
        SELECT *
        FROM asset_claim
        WHERE created_by = :user_id
        ORDER BY created_at DESC NULLS LAST
    """)

    result = db.execute(sql, {"user_id": user_id})
    return result.mappings().all()



def get_approved_asset_claims_by_user_id_sql(db: Session, user_id: str):

    sql = text("""
SELECT 
    acs.*,
    acd.sap_assets_no AS sap_assets_no
FROM asset_claim_submission acs
LEFT JOIN asset_claim_disbursement acd
    ON acs.asset_claim_submission_id = acd.asset_claim_submission_id
WHERE acs.created_by = :user_id
AND acs.status IN (
    'Asset Claim Approved',
    'Asset Claim Disbursed',
    'Asset Buyback Rejected',
    'Asset Buyback Approved'
)
""")
 
    result = db.execute(sql, {"user_id": user_id})

    return result.mappings().all()

 