from fastapi import APIRouter, Query, HTTPException

from typing import Dict, List, Optional
 
router = APIRouter(prefix="/api", tags=["Furniture Items"])
 
DATA: Dict[str, List[str]] = {

    "electronics": [

        "Air conditioner",

        "Air cooler",

        "Desert cooler",

        "Geyser",

        "Heater",

        "Water cooler",

        "Deep Freezer",

        "Refrigerator",

        "Camera",

        "Digital Diary",

        "Tripod",

        "Camcorders",

        "Bedside digital clocks",

        "Digital photo frames",

        "Ceiling fan",

        "Electric Iron",

        "Lamp",

        "Pedestal fan",

        "Pedestal Lamp",

        "Table fan",

        "Solar light appliances",

        "Cooking range",

        "Food warmer",

        "Dish Washer",

        "Electric Chimney",

        "Electric Stove",

        "Exhaust fan",

        "Gas Stove",

        "Grinder",

        "Food Processor",

        "Mixer",

        "Juicer",

        "Blender",

        "Oven",

        "Microwave",

        "Grill",

        "Toaster",

        "Coffee maker",

        "Deep fryer",

        "Electronic cooker",

        "Induction plates & cookers",

        "Rice cooker",

        "Electric Barbeque",

        "Software",

        "Modem",

        "Printer",

        "Scanner",

        "Monitor",

        "Screen guards",

        "Notebooks",

        "Tablet and book readers",

        "Data Storage device",

        "Networking modems & routers",

        "Bluetooth router",

        "Washing machine",

        "Vacuum cleaner",

        "Water filter",

        "Aqua guard",

        "Water purifier",

        "Generator set",

        "Inverter",

        "Transformer / UPS / Spike buster",

        "Stabilizer",

        "Sewing machine",

        "Hair dryer",

        "Drill machine",

        "Air purifiers",

        "Music system",

        "Record player",

        "Stereo",

        "Radio",

        "Tape recorder",

        "TV",

        "VCR",

        "VCP",

        "VCD",

        "Speaker",

        "Woofers for Home",

        "Home theatre",

        "Docking station",

        "Portable Audio Video player",

        "Satellite radio",

        "DTH",

        "Fax machine",

        "Business card reader",

        "Handheld PDA",

        "Palm Top",

        "Safety alarms",

        "CCTV cameras",

        "Smoke detectors",

        "Fire Alarms"

    ],
 
    "furniture": [

        "Round Shaped Chairs",

        "Settee",

        "Cot",

        "Service trolley",

        "Telephone stand",

        "PC trolly",

        "Almirah",

        "Bed",

        "Cane Chair",

        "Centre Table",

        "Chairs",

        "Corner table",

        "Cupboard",

        "Cabinet",

        "Dining chair",

        "Dining table",

        "Diwan",

        "Dressing table",

        "Easy chair",

        "Godrej Steel Almirah",

        "Kitchen Cabinet",

        "Pressing Stand",

        "Shoe rack",

        "Showcase",

        "Sideboard",

        "PC table",

        "Sofa Chair",

        "Sofa cum bed",

        "Sofa set",

        "Steel Almirah",

        "Steel table",

        "Stool",

        "Storwell",

        "Wall unit",

        "Wardrobe",

        "Writing table",

        "Bean bags",

        "Coat Stand",

        "Wall clock",

        "Wall piece",

        "Vases",

        "Candles",

        "Table tops",

        "Fountains",

        "Sculptures",

        "Wall decors",

        "Mirrors",

        "Chandeliers",

        "Lighting accessories",

        "Display accessories"

    ],
 
    "soft_furnishing": [

        "Carpet / Curtain",

        "Cushion",

        "Mattress"

    ],
 
    "sports_equipment": [

        "Stepper",

        "Jogger",

        "Cross trainer",

        "Treadmill"

    ]

}

@router.get("/get/furniture/items")

def get_items(

    category: Optional[str] = Query(None, description="electronics / furniture / soft_furnishing / sports_equipment")

):

    # If no category → return everything

    if not category:

        return {

            "status": "success",

            "data": DATA

        }
 
    category = category.lower()
 
    if category not in DATA:

        raise HTTPException(status_code=404, detail="Invalid category")
 
    return {

        "status": "success",

        "category": category,

        "items": DATA[category]

    }

 

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

router = APIRouter()

# @router.get("/asset-claims/dropdown/items")

# def get_item_dropdown(

#     user_id: int = Query(..., description="Logged-in user ID"),

#     db: Session = Depends(get_db)

# ):

#     query = text("""

#         SELECT DISTINCT

#             acs.item_type,

#             acs.item_name,

#             acs.amount_to_be_disbursed

#         FROM asset_claim ac

#         JOIN asset_claim_submission acs

#             ON ac.asset_claim_id = acs.asset_claim_id

#         WHERE ac.created_by = :user_id

#           AND ac.bought_back = FALSE

#           AND (

#                 acs.status ILIKE '%approved%'

#                 OR acs.status ILIKE '%disbursed%'

#               )

#           AND acs.item_type IS NOT NULL

#           AND acs.item_name IS NOT NULL

#         ORDER BY acs.item_type, acs.item_name

#     """)
 
#     result = db.execute(query, {"user_id": user_id}).fetchall()
 
#     return {

#         "status": "success",

#         "count": len(result),

#         "data": [

#             {

#                 "item_type": row.item_type,

#                 "item_name": row.item_name,

#                 "amount_to_be_disbursed": float(row.amount_to_be_disbursed)

#                 if row.amount_to_be_disbursed is not None else 0.0

#             }

#             for row in result

#         ]

# }
 

# @router.get("/asset-claims/dropdown/items")
# def get_item_dropdown(
#     user_id: int = Query(..., description="Logged-in user ID"),
#     db: Session = Depends(get_db)
#     ):
#     query = text("""
#         SELECT DISTINCT
#             acs.item_type,
#             acs.item_name,
#             acs.amount_to_be_disbursed
#         FROM asset_claim ac
#         JOIN asset_claim_submission acs
#             ON ac.asset_claim_id = acs.asset_claim_id
#         WHERE ac.created_by = :user_id
#           AND ac.bought_back = FALSE
#           AND ac.category = 'Furniture'               -- ✅ CATEGORY FILTER
#           AND (
#                 acs.status ILIKE '%approved%'
#                 OR acs.status ILIKE '%disbursed%'
#               )
#           AND acs.item_type IS NOT NULL
#           AND acs.item_name IS NOT NULL
#         ORDER BY acs.item_type, acs.item_name
#     """)

#     result = db.execute(query, {"user_id": user_id}).fetchall()

#     return {
#         "status": "success",
#         "count": len(result),
#         "data": [
#             {
#                 "item_type": row.item_type,
#                 "item_name": row.item_name,
#                 "amount_to_be_disbursed": float(row.amount_to_be_disbursed)
#                 if row.amount_to_be_disbursed is not None else 0.0
#             }
#             for row in result
#         ]
#     }

@router.get("/asset-claims/dropdown/items")
def get_item_dropdown(
    user_id: int = Query(..., description="Logged-in user ID"),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT DISTINCT
            acs.item_type,
            acs.item_name,
            (acs.item_type || ' - ' || acs.item_name) AS furniture_name,
            acs.amount_to_be_disbursed
        FROM asset_claim ac
        JOIN asset_claim_submission acs
            ON ac.asset_claim_id = acs.asset_claim_id
        WHERE ac.created_by = :user_id
          AND ac.bought_back = FALSE
          AND ac.category = 'Furniture'
          AND (
                acs.status ILIKE '%approved%'
                OR acs.status ILIKE '%disbursed%'
              )
          AND acs.item_type IS NOT NULL
          AND acs.item_name IS NOT NULL
        ORDER BY acs.item_type, acs.item_name
    """)

    result = db.execute(query, {"user_id": user_id}).fetchall()

    return {
        "status": "success",
        "count": len(result),
        "data": [
            {
                "item_type": row.item_type,
                "item_name": row.item_name,
                "furniture_name": row.furniture_name,   # ✅ NEW FIELD
                "amount_to_be_disbursed": float(row.amount_to_be_disbursed)
                if row.amount_to_be_disbursed is not None else 0.0
            }
            for row in result
        ]
    }




@router.get("/furniture-reimbursement-amount")
def get_furniture_reimbursement(
    furniture_name: str = Query(...),
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            fr.furniture_rm_reimbursement_id,
            fr.furniture_name,
            fr.claim_month_year,
            fr.eligible_amount,
            fr.amount_claimed,
            COALESCE(fr.eligible_amount, 0) 
              - COALESCE(fr.amount_claimed, 0) AS available_amount,
            fr.status,
            fr.remarks
        FROM furniture_rm_reimbursement fr
        JOIN ra_claim rc
            ON rc.ra_claim_id = fr.ra_claim_id
        WHERE fr.furniture_name ILIKE :furniture_name
          AND rc.created_by = :user_id
    """)

    result = db.execute(
        query,
        {
            "furniture_name": f"%{furniture_name}%",
            "user_id": user_id
        }
    ).fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="No furniture reimbursement data found")

    return {
        "count": len(result),
        "data": [
            {
                "furniture_rm_reimbursement_id": row.furniture_rm_reimbursement_id,
                "furniture_name": row.furniture_name,
                "claim_month_year": row.claim_month_year,
                "eligible_amount": row.eligible_amount,
                "amount_claimed": row.amount_claimed,
                "available_amount": row.available_amount,
                "status": row.status,
                "remarks": row.remarks,
            }
            for row in result
        ]
    }