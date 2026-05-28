from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.database import Base

class UnknownFace(Base):
    __tablename__ = "unknown_faces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    device_id = Column(UUID(as_uuid=True), nullable=False)
    snapshot_path = Column(String(500), nullable=True)
    confidence = Column(Float, nullable=True)
    captured_at = Column(DateTime, default=datetime.utcnow)
