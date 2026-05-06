from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.circular_management.category_master_schema import (CategoryCreate, CategoryUpdate)
from app.crud.circular_management.category_master_crud import (create_category, delete_category, get_all_category, get_all_category_subcategory, get_category, update_category)

router = APIRouter(
    prefix="/category-master",
    tags=["Category Master"]
)


@router.post("/create")
def create_category_api(data: CategoryCreate, db: Session = Depends(get_db)):
    category_id = create_category(db, data)
    return {
        "status": "success",
        "category_id": category_id
    }


@router.put("/update/{category_id}")
def update_category_api(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    update_category(db, category_id, data)
    return {"status": "success","message": "Category updated successfully"}


# @router.delete("/{category_id}", response_model=dict)
# def delete_category_api(
#     category_id: int,
#     deleted_by: int,
#     db: Session = Depends(get_db)
# ):
#     delete_category(db, category_id, deleted_by)
#     return {"message": "Category deleted successfully"}


# @router.get("/", response_model=list)
# def get_all_categories_api(db: Session = Depends(get_db)):
#     return get_all_categories(db)

@router.get("/get/{category_id}")
def get(category_id: int, db: Session = Depends(get_db)):
    result = get_category(db, category_id)
    return result

@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    result = get_all_category(db)
    return result

@router.get("/categories-with-subcategories")
def get_all_categories(db: Session = Depends(get_db)):
    return get_all_category_subcategory(db)

@router.delete("/delete/{category_id}")
def delete_category_api(
    category_id: int,
    deleted_by: int,
    db: Session = Depends(get_db)
):
    success = delete_category(db, category_id, deleted_by)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Category not found or already deleted"
        )

    return {
        "status": "success",
        "message": "Category and related subcategories deleted successfully"
    }