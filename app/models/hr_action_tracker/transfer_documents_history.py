import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class TransferDocumentHistory(Base):
    __tablename__ = "transfer_documents_history"
    history_id = Column(Integer, primary_key=True, index=True)
    id= Column(Integer, nullable=True)
    transfer_id = Column(Integer, ForeignKey("employee_transfers.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)