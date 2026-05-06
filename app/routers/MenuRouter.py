from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import MenuCrud
from app.utils.UserAuthUtils import verify_access_token  #  import this

router = APIRouter(prefix="/api/Menu", tags=["Menu"])

@router.get("")
def get_menus(
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)  #  check token
):
    return MenuCrud.get_all_menus(db)
