# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.crud.employees_info.declaration_settings import create_declaration_setting, get_all_declaration_settings, update_declaration_setting
# from app.database import get_db
# from app.schemas.employees_info.declaration_settings import DeclarationSettingsCreate, DeclarationSettingsOut, DeclarationSettingsUpdate


# router = APIRouter(prefix="/api/declaration", tags=["Declaration Gloabal setting "])


# # ---------------------------
# # GET ALL
# # ---------------------------
# @router.get("/", response_model=list[DeclarationSettingsOut])
# def route_get_all(db: Session = Depends(get_db)):
#     return get_all_declaration_settings(db)


# # ---------------------------
# # CREATE (POST)
# # ---------------------------
# @router.post("/", response_model=DeclarationSettingsOut)
# def route_create(payload: DeclarationSettingsCreate, db: Session = Depends(get_db)):
#     return create_declaration_setting(db, payload.dict())


# # ---------------------------
# # UPDATE (PUT)
# # ---------------------------
# @router.put("/{dec_id}", response_model=DeclarationSettingsOut)
# def route_update(dec_id: int, payload: DeclarationSettingsUpdate, db: Session = Depends(get_db)):
#     updated = update_declaration_setting(db, dec_id, payload.dict(exclude_unset=True))

#     if not updated:
#         raise HTTPException(404, detail="Declaration setting not found")

#     return updated


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.crud.employees_info.declaration_settings import create_declaration_setting, get_all_declaration_settings, update_declaration_setting
# from app.database import get_db
# from app.schemas.employees_info.declaration_settings import DeclarationSettingsCreate, DeclarationSettingsOut, DeclarationSettingsUpdate


from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.crud.employees_info.declaration_settings_notification_crud import handle_declaration_setting
from app.database import get_db

from app.schemas.employees_info.declaration_settings import (
    DeclarationSettingsCreate,
    DeclarationSettingsOut,
    DeclarationSettingsUpdate
)


from app.crud.employees_info.declaration_settings import (
    get_all_declaration_settings,
    update_declaration_setting
)

router = APIRouter(prefix="/api/declaration", tags=["Declaration Global Setting"])


# ---------------------------
# GET ALL
# ---------------------------
@router.get("/all", response_model=list[DeclarationSettingsOut])
def route_get_all(db: Session = Depends(get_db)):
    return get_all_declaration_settings(db)


# ---------------------------
# CREATE (Broadcast Enabled)
# ---------------------------
@router.post("/create", response_model=DeclarationSettingsOut)
async def route_create(
    payload: DeclarationSettingsCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return await handle_declaration_setting(
        db=db,
        data=payload.dict(),
        background_tasks=background_tasks
    )


# ---------------------------
# UPDATE (Optional)
# ---------------------------
@router.put("/{dec_id}", response_model=DeclarationSettingsOut)
def route_update(
    dec_id: int,
    payload: DeclarationSettingsUpdate,
    db: Session = Depends(get_db)
):
    updated = update_declaration_setting(
        db,
        dec_id,
        payload.dict(exclude_unset=True)
    )

    if not updated:
        raise HTTPException(404, detail="Declaration setting not found")

    return updated


    