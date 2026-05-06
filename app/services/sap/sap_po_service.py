from fastapi import HTTPException
from app.services.sap.sap_session import sap_session, SAP_BASE_URL


def get_po_dropdown():
    """
    PO Dropdown → PO_F4Set
    """
    try:
        url = f"{SAP_BASE_URL}/PO_F4Set"
        response = sap_session.get(url, params={"$format": "json"})
        response.raise_for_status()

        return response.json().get("d", {}).get("results", [])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_po_details(ebeln: str):
    """
    PO Line Items → PO_DetailSet
    """
    try:
        url = f"{SAP_BASE_URL}/PO_DetailSet"
        params = {
            "$filter": f"Ebeln eq '{ebeln}'",
            "$format": "json"
        }

        response = sap_session.get(url, params=params)
        response.raise_for_status()

        return response.json().get("d", {}).get("results", [])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
