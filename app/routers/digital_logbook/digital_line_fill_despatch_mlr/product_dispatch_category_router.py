from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token

# Schemas
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_schema import (
    ProductDispatchCategoryCreate,
    ProductDispatchCategoryUpdate,
    ProductDispatchCategoryResponse,
)

from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_hourly_log_schema import (
    ProductDispatchHourlyMasterResponse,
    ProductDispatchHourlyDateSearch,
)
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shutdown_log_schema import (
    ProductDispatchShutdownMasterResponse,
    ProductDispatchShutdownDateSearch,
)

from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_log_schema import (
    ProductDispatchShiftLogDateSearch,
    ProductDispatchShiftLogMasterResponse,
)


# CRUD
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_crud import (
    create_product_dispatch_category,
    update_product_dispatch_category,
    delete_product_dispatch_category,
    get_product_dispatch_category_with_names,
    get_combined_hourly_by_date,
    get_combined_shutdown_by_date,
    get_combined_shift_log_by_date,
    get_shift_log_by_master_id,
    get_category_master_by_date,
)
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_hourly_log_crud import (
    get_hourly_logs_by_master_id,
)
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shutdown_log_crud import (
    get_shutdown_logs_by_master_id,
)

router = APIRouter(
    prefix="/product-dispatch-category",
    tags=["Product Dispatch Category"],
    dependencies=[Depends(validate_token)],
)

# --- REUSABLE HELPERS ---


def get_or_404(data, message="Not found"):
    if not data:
        raise HTTPException(status_code=404, detail=message)
    return data


def check_update(result, message="No fields provided for update"):
    if not result:
        raise HTTPException(status_code=400, detail=message)


def check_delete(result, message="Product dispatch category not found"):
    if not result:
        raise HTTPException(status_code=404, detail=message)


def fetch_master_data(func, db, master_id, *args, message="Master not found"):
    data = func(db, master_id, *args)
    return get_or_404(data, message)


# --- ROUTE HANDLERS ---


@router.post("")
def create_product_dispatch_category_api(
    payload: ProductDispatchCategoryCreate, db: Session = Depends(get_db)
):
    category_id = create_product_dispatch_category(db, payload)
    return {
        "message": "Product dispatch category created successfully",
        "p_category_master_id": category_id,
    }


@router.put("/{p_category_master_id}")
def update_product_dispatch_category_api(
    p_category_master_id: int,
    payload: ProductDispatchCategoryUpdate,
    db: Session = Depends(get_db),
):
    result = update_product_dispatch_category(db, p_category_master_id, payload)
    check_update(result)
    return {"message": "Product dispatch category updated successfully"}


@router.delete("/{p_category_master_id}")
def delete_product_dispatch_category_api(
    p_category_master_id: int, db: Session = Depends(get_db)
):
    result = delete_product_dispatch_category(db, p_category_master_id)
    check_delete(result)
    return {"message": "Product dispatch category deleted successfully"}


@router.get("/{p_category_master_id}", response_model=ProductDispatchCategoryResponse)
def get_product_dispatch_category_api(
    p_category_master_id: int, db: Session = Depends(get_db)
):
    """Fetch only the master data for a specific category ID (no child entries)."""
    return fetch_master_data(
        get_product_dispatch_category_with_names, db, p_category_master_id
    )


@router.get("/date-search/master", response_model=List[ProductDispatchCategoryResponse])
def get_category_master_by_date_api(search_date: date, db: Session = Depends(get_db)):
    """Fetch only master records for a specific logbook date."""
    return get_category_master_by_date(db, search_date)


@router.get("/date-search/hourly", response_model=List[ProductDispatchHourlyDateSearch])
def get_combined_hourly_api(search_date: date, db: Session = Depends(get_db)):
    """Fetch combined Hourly logs with 7 AM - 7 AM operational window."""
    return get_combined_hourly_by_date(db, search_date)


@router.get(
    "/date-search/shutdown", response_model=List[ProductDispatchShutdownDateSearch]
)
def get_combined_shutdown_api(search_date: date, db: Session = Depends(get_db)):
    return get_combined_shutdown_by_date(db, search_date)


@router.get(
    "/date-search/shift-log", response_model=List[ProductDispatchShiftLogDateSearch]
)
def get_combined_shift_log_api(
    search_date: date, shift_id: int, db: Session = Depends(get_db)
):
    return get_combined_shift_log_by_date(db, search_date, shift_id)


@router.get(
    "/{p_category_master_id}/hourly", response_model=ProductDispatchHourlyMasterResponse
)
def get_master_hourly_api(p_category_master_id: int, db: Session = Depends(get_db)):
    return fetch_master_data(get_hourly_logs_by_master_id, db, p_category_master_id)


@router.get(
    "/{p_category_master_id}/shutdown",
    response_model=ProductDispatchShutdownMasterResponse,
)
def get_master_shutdown_api(p_category_master_id: int, db: Session = Depends(get_db)):
    """Fetch consolidated Master + Shutdown entries for a specific master ID."""
    return fetch_master_data(get_shutdown_logs_by_master_id, db, p_category_master_id)


@router.get(
    "/{p_category_master_id}/shift-log",
    response_model=ProductDispatchShiftLogMasterResponse,
)
def get_master_shift_log_api(
    p_category_master_id: int, shift_id: int, db: Session = Depends(get_db)
):
    return fetch_master_data(
        get_shift_log_by_master_id, db, p_category_master_id, shift_id
    )
