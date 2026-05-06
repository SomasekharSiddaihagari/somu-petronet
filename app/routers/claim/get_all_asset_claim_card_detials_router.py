from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.claim.get_all_asset_claim_details_crud import get_asset_entitlement
from app.schemas.claim.get_all_asset_claim_details_schema import AssetEntitlementResponse
from app.schemas.gate_pass.GatePass import AssetDashboardResponse



router = APIRouter(
    prefix="/get-all-asset-claim_card_details",
    tags=["Asset Claim"],
)


@router.get(
    "/entitlement",
    response_model=AssetEntitlementResponse,
)
def get_asset_entitlement_api(
    user_id: int,
    category: str,
    item_type: str,
    sub_category: Optional[str] = None,   # ✅ ADD THIS
    db: Session = Depends(get_db),
):
    try:
        return get_asset_entitlement(
            db=db,
            user_id=user_id,
            category=category,
            item_type=item_type,
            sub_category=sub_category,     # ✅ PASS IT
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get(
    "/entitlement/dashboard",
    response_model=AssetDashboardResponse,
)
def get_asset_dashboard(
    user_id: int,
    db: Session = Depends(get_db),
):
    try:
        mobile = get_asset_entitlement(
            db=db,
            user_id=user_id,
            category="Mobile Handset",
            item_type="Mobile Handset",
        )

        laptop = get_asset_entitlement(
            db=db,
            user_id=user_id,
            category="Laptop / Desktop",
            item_type="Laptop",
        )

        data_card = get_asset_entitlement(
            db=db,
            user_id=user_id,
            category="Data Card",
            item_type="Data Card",
        )

        # Furniture needs sub_category — fetch both variants
        furniture_utility = get_asset_entitlement(
            db=db,
            user_id=user_id,
            category="Furniture",
            item_type="Furniture",
            sub_category="Utility & Decorative Furniture",
        )

        furniture_office = get_asset_entitlement(
            db=db,
            user_id=user_id,
            category="Furniture",
            item_type="Furniture",
            sub_category="Office Furniture",
        )

        return {
            "user_id": user_id,
            "dashboard": {
                "mobile_handset": mobile,
                "laptop_desktop": laptop,
                "data_card": data_card,
                "furniture": {
                    "utility_decorative": furniture_utility,
                    "office": furniture_office,
                },
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
