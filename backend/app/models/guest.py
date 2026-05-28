from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum
from app.database import Base

class GuestType(str, enum.Enum):
    REGULAR = "regular"
    VIP = "vip"
    STAFF = "staff"
    MEDIA = "media"
    VENDOR = "vendor"
    SPEAKER = "speaker"

class Guest(Base):
    __tablename__ = "guests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guest_code = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=True)
    email = Column(String(200), nullable=True)
    company = Column(String(200), nullable=True)
    designation = Column(String(200), nullable=True)
    guest_type = Column(Enum(GuestType), default=GuestType.REGULAR)
    is_vip = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    # Face recognition data
    photo_paths = Column(JSON, default=list)
    face_embedding = Column(JSON, nullable=True)
    face_embeddings_all = Column(JSON, default=list)
    embedding_model = Column(String(50), default="buffalo_l")

    # QR
    qr_token = Column(String(64), unique=True, nullable=True)
    qr_image_path = Column(String(500), nullable=True)

    # Meta
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Relationships
    event_mappings = relationship("EventGuest", back_populates="guest")
    attendance_logs = relationship("AttendanceLog", back_populates="guest")


class EventGuest(Base):
    """Many-to-many: guest ↔ event mapping"""
    __tablename__ = "event_guests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"))
    is_vip_override = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    event = relationship("Event", back_populates="guest_mappings")
    guest = relationship("Guest", back_populates="event_mappings")


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    verify_mode = Column(String(20))
    confidence = Column(Float, nullable=True)
    snapshot_path = Column(String(500), nullable=True)
    is_duplicate = Column(Boolean, default=False)
    entry_time = Column(DateTime, default=datetime.utcnow)
    gate_label = Column(String(100), nullable=True)
    
    guest = relationship("Guest", back_populates="attendance_logs")
