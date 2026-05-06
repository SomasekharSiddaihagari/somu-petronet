from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token

# Schemas
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shutdown_log_schema import (
    ProductDispatchShutdownCreate,
    ProductDispatchShutdownUpdate,
    ProductDispatchShutdownResponse,
)

# CRUD
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shutdown_log_crud import (
    create_product_dispatch_shutdown,
    update_product_dispatch_shutdown,
    delete_product_dispatch_shutdown,
    get_shutdown_log_by_id,
    get_latest_cumulative_balance_summary,  # <-- Renamed
)

router = APIRouter(
    prefix="/product-dispatch-shutdown",
    tags=["Product Dispatch Shutdown Log"],
    dependencies=[Depends(validate_token)],
)



@router.post("")
def create_product_dispatch_shutdown_api(
    payload: ProductDispatchShutdownCreate,
    db: Session = Depends(get_db)
):
    shutdown_id = create_product_dispatch_shutdown(db, payload)
    return {
        "message": "Product dispatch shutdown log created successfully",
        "p_dispatch_shutdown_id": shutdown_id,
    }


@router.put("/{p_dispatch_shutdown_id}")
def update_product_dispatch_shutdown_api(
    p_dispatch_shutdown_id: int,
    payload: ProductDispatchShutdownUpdate,
    db: Session = Depends(get_db),
):
    updated = update_product_dispatch_shutdown(db, p_dispatch_shutdown_id, payload)
    if not updated:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return {"message": "Product dispatch shutdown log updated successfully"}


@router.delete("/{p_dispatch_shutdown_id}")
def delete_product_dispatch_shutdown_api(
    p_dispatch_shutdown_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_product_dispatch_shutdown(db, p_dispatch_shutdown_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Product dispatch shutdown log not found"
        )

    return {"message": "Product dispatch shutdown log deleted successfully"}


@router.get("/cumulative-balance")
def get_cumulative_balance_api(
    search_date: date = Query(None), 
    db: Session = Depends(get_db)
):
    """
    Dashboard API: Returns the shutdown balance for ALL stations as of a specific date.
    Strictly date-based.
    """
    effective_date = search_date or date.today()
    result = get_latest_cumulative_balance_summary(db, effective_date)
    
    return {
        "status": "success",
        "as_of_date": effective_date,
        "cumulative_balance": result
    }


@router.get("/{p_dispatch_shutdown_id}", response_model=ProductDispatchShutdownResponse)
def get_shutdown_log_api(
    p_dispatch_shutdown_id: int,
    db: Session = Depends(get_db)
):
    data = get_shutdown_log_by_id(db, p_dispatch_shutdown_id)
    if not data:
        raise HTTPException(
            status_code=404, detail="Product dispatch shutdown log not found"
        )
    return data
