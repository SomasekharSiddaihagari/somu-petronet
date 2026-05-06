from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String, nullable=False)
    menu_url = Column(String, nullable=True)
    menu_icon = Column(String, nullable=True)

    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete-orphan")
    permissions = relationship("RolePermission", back_populates="menu")


class SubMenu(Base):
    __tablename__ = "submenus"

    submenu_id = Column(Integer, primary_key=True, index=True)
    submenu_name = Column(String, nullable=False)
    submenu_url = Column(String, nullable=True)
    submenu_icon = Column(String, nullable=True)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)

    menu = relationship("Menu", back_populates="submenus")
    permissions = relationship("RolePermission", back_populates="submenu")
