from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import SubMenuCrud
from app.utils.UserAuthUtils import verify_access_token  # check token

router = APIRouter(prefix="/api/SubMenus", tags=["SubMenu"])

@router.get("")
def get_submenus(
    db: Session = Depends(get_db),
     current_user: str = Depends(verify_access_token)  # JWT token verification
):
    return SubMenuCrud.get_all_submenus(db)
