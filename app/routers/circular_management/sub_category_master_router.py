from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.circular_management.sub_category_master_crud import create_subcategory, delete_subcategory, get_all_subcategory, get_subcategory, update_subcategory
from app.database import get_db
from app.schemas.circular_management.sub_category_master_schema import SubCategoryCreate, SubCategoryUpdate
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/subcategory-master",
    tags=["SubCategory Master"])


@router.post("/create")
def create_subcategory_api(data: SubCategoryCreate,db: Session = Depends(get_db)
):
    subcategory_id = create_subcategory(db, data)
    return {
        "status": "success",
        "subcategory_id": subcategory_id
    }


@router.put("/update/{subcategory_id}")
def update_subcategory_api(subcategory_id: int,data: SubCategoryUpdate,db: Session = Depends(get_db)):
    update_subcategory(db, subcategory_id, data)
    return {
        "status": "success",
        "message": "Subcategory updated successfully"
    }


@router.get("/get/{subcategory_id}")
def get_by_id(subcategory_id: int,db: Session = Depends(get_db)):
    result = get_subcategory(db, subcategory_id)
    return result


@router.get("/get-all")
def get_all(db: Session = Depends(get_db)):
    result = get_all_subcategory(db)
    return result


@router.delete("/delete/{subcategory_id}")
def delete_subcategory_api(
    subcategory_id: int,
    db: Session = Depends(get_db)
):
    delete_subcategory(db, subcategory_id)
    return {
        "status": "success",
        "message": "Subcategory deleted successfully"
    }
