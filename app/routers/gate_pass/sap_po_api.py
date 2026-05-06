from fastapi import APIRouter
from app.services.sap.sap_po_service import (
    get_po_dropdown,
    get_po_details
)

router = APIRouter(
    prefix="/api/sap/po",
    tags=["SAP PO"]
)


@router.get("/dropdown")
def po_dropdown():
    return get_po_dropdown()


@router.get("/details/{ebeln}")
def po_details(ebeln: str):
    return get_po_details(ebeln)
