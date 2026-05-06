from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    created_by = Column(String(100), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    modified_by = Column(String(100), nullable=True)
    modified_date = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    permissions = relationship("RolePermission", back_populates="role")
    users = relationship("User", back_populates="role")
