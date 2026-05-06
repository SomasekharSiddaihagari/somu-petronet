from sqlalchemy.orm import Session
from app.models.MenuModel import SubMenu

def get_all_submenus(db: Session):
    submenus = db.query(SubMenu).all()

    data = []
    for sm in submenus:
        data.append({
            "submenu_id": sm.submenu_id,
            "submenu_name": sm.submenu_name,
            "submenu_url": sm.submenu_url or "",
            "submenu_icon": sm.submenu_icon or "",
            "menu_id": sm.menu_id
        })

    response = {
        "status_code": "0000",
        "status_message": "success",
        "data": data
    }

    return response
