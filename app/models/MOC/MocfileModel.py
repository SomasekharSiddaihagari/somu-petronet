from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class File(Base):
    __tablename__ = "moc_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    # filetype = Column(String, nullable=True)
    model_id = Column(Integer, nullable=False, index=True)
    model_name = Column(String(120), nullable=False, index=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
