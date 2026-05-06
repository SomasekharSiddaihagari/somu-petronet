from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token

# Schemas
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_hourly_log_schema import (
    ProductDispatchHourlyCreate,
    ProductDispatchHourlyUpdate,
    ProductDispatchHourlyResponse
)

# CRUD
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_hourly_log_crud import (
    create_product_dispatch_hourly,
    update_product_dispatch_hourly,
    delete_product_dispatch_hourly,
    get_hourly_log_by_id
)

router = APIRouter(
    prefix="/product-dispatch-hourly",
    tags=["Product Dispatch Hourly"],
    dependencies=[Depends(validate_token)],
)

@router.post("")
def create_product_dispatch_hourly_api(
    payload: ProductDispatchHourlyCreate,
    db: Session = Depends(get_db)
):
    hour_id = create_product_dispatch_hourly(db, payload)
    return {
        "message": "Product dispatch hourly log created successfully",
        "p_dispatch_hour_id": hour_id
    }

@router.put("/{p_dispatch_hour_id}")
def update_product_dispatch_hourly_api(
    p_dispatch_hour_id: int,
    payload: ProductDispatchHourlyUpdate,
    db: Session = Depends(get_db)
):
    updated = update_product_dispatch_hourly(db, p_dispatch_hour_id, payload)
    if not updated:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return {"message": "Product dispatch hourly log updated successfully"}

@router.delete("/{p_dispatch_hour_id}")
def delete_product_dispatch_hourly_api(
    p_dispatch_hour_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_product_dispatch_hourly(db, p_dispatch_hour_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product dispatch hourly log not found")

    return {"message": "Product dispatch hourly log deleted successfully"}

@router.get("/{p_dispatch_hour_id}", response_model=ProductDispatchHourlyResponse)
def get_hourly_log_api(
    p_dispatch_hour_id: int,
    db: Session = Depends(get_db)
):
    data = get_hourly_log_by_id(db, p_dispatch_hour_id)
    if not data:
        raise HTTPException(status_code=404, detail="Product dispatch hourly log not found")
    return data
