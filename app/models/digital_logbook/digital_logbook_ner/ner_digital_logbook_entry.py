from sqlalchemy import Column, Integer, String, Time, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class NerDigitalLogBookEntry(Base):
    __tablename__ = "ner_digital_logbook_entry"

    ner_entry_id = Column(Integer, primary_key=True, autoincrement=True)

    ner_logbook_id = Column(
        Integer,
        ForeignKey("ner_digital_logbook.ner_logbook_id", ondelete="CASCADE"),
        nullable=True,
    )

    entry_time = Column(Time, nullable=True)
    location = Column(String(100), nullable=True)

    # 🔥 NEW FIELD
    logs = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
