from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class CircularAttachmentHistory(Base):
    __tablename__ = "circular_attachments_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    attachment_id = Column(
        Integer,
        nullable=True
    )
 
    circular_id = Column(
        Integer,
        ForeignKey("circular_master.circular_id", ondelete="CASCADE"),
        nullable=False
    )
 
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_size = Column(BigInteger, nullable=True)
 
    uploaded_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )
 
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    version = Column(String(20), nullable=True)