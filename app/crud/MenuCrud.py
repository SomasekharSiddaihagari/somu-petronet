from sqlalchemy.orm import Session
from app.models.MenuModel import Menu, SubMenu

def get_all_menus(db: Session):
    menus = db.query(Menu).all()

    data = []
    for menu in menus:
        submenu_list = [
            {
                "submenu_id": sm.submenu_id,
                "submenu_name": sm.submenu_name,
                "submenu_url": sm.submenu_url or "",
                "submenu_icon": sm.submenu_icon or ""
            }
            for sm in menu.submenus
        ]

        data.append({
            "menu_id": menu.menu_id,
            "menu_name": menu.menu_name,
            "menu_url": menu.menu_url or "",
            "menu_icon": menu.menu_icon or "",
            "submenu_list": submenu_list
        })

    response = {
        "status_code": "0000",
        "status_message": "success",
        "data": data
    }

    return response
