from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class RolePermission(Base):

    __tablename__ = "role_permissions"
 
    rp_id = Column(Integer, primary_key=True, index=True)
 
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)

    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)

    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=True)

    submenu_id = Column(Integer, ForeignKey("submenus.submenu_id"), nullable=True)
 
    role = relationship("Role", back_populates="permissions")

    submenu = relationship("SubMenu", back_populates="permissions")
    menu = relationship("Menu", back_populates="permissions")  
    user = relationship("User", back_populates="permissions")

 