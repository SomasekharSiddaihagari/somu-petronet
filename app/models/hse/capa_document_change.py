from sqlalchemy import Column, DateTime, ForeignKey, ForeignKey, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

from app.models.hse.hse_incident_capa_actions import Base

from app.database import Base

class CapaDocumentChange(Base):
    __tablename__ = "capa_document_change"
 
    capa_doc_id = Column(Integer, primary_key=True, autoincrement=True)
    capa_id = Column(Integer, ForeignKey("capa_report.capa_report_id"), nullable=False)
 
    document_code = Column(String(100), nullable=True)
    changes_in_brief = Column(String(500), nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
