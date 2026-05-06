from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database import Base

class ResetPasswordModel(Base):
    __tablename__ = "reset_password"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    email = Column(String, nullable=False)
    reset_token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=30))
    used = Column(Boolean, default=False)

    user = relationship("User")